import re
from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.app.portlets.portlets.login import Renderer as LoginPortletRenderer
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.schema.interfaces import ITextLine
from zope.formlib import form
from zope.formlib.textwidgets import TextWidget
from Products.CMFCore.Expression import createExprContext, Expression
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PythonScripts.standard import html_quote

from collective.aaf import aafMessageFactory as _
from collective.aaf import utils

from zope.i18nmessageid import MessageFactory
__ = MessageFactory("plone")


class ITALESTextLine(ITextLine):
    """ Marker interface for TALES fields.
    """
    pass

class TALESTextLine(schema.TextLine):
    implements(ITALESTextLine)

class LongTextWidget(TextWidget):
    displayWidth = 70


class IShibbolethLoginPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(
        title=__(u"Portlet header"),
        description=__(u"Title of the rendered portlet"),
        constraint=re.compile("[^\s]").match,
        default=u"AAF (Institutional)",
        required=True)

    wayf_URL = TALESTextLine(
        title=_(u"WAYF Discovery URL (TALES)"),
        description=_(u"URL of the WAYF to use"),
        default=u"string:https://ds.aaf.edu.au/discovery/DS",
        required=True)

    wayf_sp_entityID = TALESTextLine(
        title=_(u"Service Provider EntityID (TALES)"),
        description=_(u"""
EntityID of the Service Provider that protects this Resource.
Value will be overwritten automatically if the page where the Embedded WAYF
is displayed is called with a GET argument 'entityID' as automatically set by Shibboleth"""),
        default=u"string:https://my-app.example.edu.au/shibboleth",
        required=True)

#// [Mandatory, if wayf_use_discovery_service = false]
    wayf_sp_handlerURL = TALESTextLine(
        title=_(u"Service Provider Handler URL (TALES)"),
        description=_(u"URL to the Shibboleth handler for the given Service Provider."),
        default=u"string:${portal_url}/Shibboleth.sso",
        required=False)

    wayf_return_url = TALESTextLine(
        title=_(u"Return URL (TALES)"),
        description=_(u"URL on this resource that the user shall be returned to after authentication"),
        default=u"string:${view/return_url}",
        required=True)




class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IShibbolethLoginPortlet)

    header = u"AAF (Institutional)"
    wayf_URL = u"string:https://ds.aaf.edu.au/discovery/DS"
    wayf_sp_entityID = u"string:https://my-app.example.edu.au/shibboleth"
    wayf_sp_handlerURL = u"string:${portal_url}/Shibboleth.sso"
    wayf_return_url = u"string:${view/return_url}"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header

def execute_expression(expr, folder, portal, object=None, **kwargs):
    """ Execute and expand a given TALES `expr`.

    Because the way in which portlets are rendered, the context needs
    to be corrected to be the surrounding folder.

    Also accepts arbitrary kwargs and applies them into the expression
    context for execution.
    """
    ec = createExprContext(folder, portal, object)
    ec.contexts['context'] = ec.contexts['here']
    for key, value in kwargs.iteritems():
        ec.setLocal(key, value)
    return Expression(expr)(ec)

class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('shibbolethloginportlet.pt')

    def __init__(self, context, request, view, manager, data):
        super(Renderer, self).__init__(context, request, view, manager, data)
        self.portal_state = getMultiAdapter((context, request),
                                            name='plone_portal_state')
        self.portal = self.portal_state.portal()

    def show(self):
        """ Determine if this portlet should be shown or not.
        """
        if not self.portal_state.anonymous():
            return False
        page = self.request.get('URL', '').split('/')[-1]
        return page not in ('login_form', '@@register')

    def _execute_expression(self, value):
        """ Execute an expression in the context of this renderer.
        """
        return execute_expression(value,
                                  self.context,
                                  self.portal,
                                  view=self)

    def embed_url(self):
        """ Generate the JavaScript embed URL for the federation.
        """
        return self._execute_expression(self.data.wayf_URL) + '/embedded-wayf.js'

    def login_url(self):
        """ Generate a suitable login URL for non-JavaScript users.

        The final ``target`` in the URL will be where the user is
        redirected to from Shibboleth.
        """
        return self._execute_expression(self.data.wayf_sp_handlerURL) \
                + '/Login?target=' + self.return_url()

    def return_url(self):
        """ Generate a suitable return URL to the current context.

        The query string is passed along here for the ride because
        the final ``logged_in`` script will redirect the user accordingly
        to the actual content item.
        """
        url = self.portal_state.navigation_root_url() + '/logged_in'
        if self.request.QUERY_STRING:
            if self.request.QUERY_STRING.endswith('/logged_out'):
                self.request.QUERY_STRING = self.request.QUERY_STRING.replace('/logged_out', '')
            url += '?' + self.request.QUERY_STRING
        return url

    def wayf_options(self):
        """ Generate JavaScript variables for the Embedded WAYF script.

        Interpolates the TALES fields with the relevant values to produce
        suitable output variables for configuration.
        """
        output = ""
        for name, field in \
            schema.getFields(IShibbolethLoginPortlet).iteritems():
            if name.startswith('wayf_'):
                value = getattr(self.data, name)
                if ITALESTextLine.providedBy(field):
                    value = self._execute_expression(value)
                output += 'var %s = %s;\n' % (name,
                                              utils.escape_javascript(value))
        return output


#Customise field display length
form_fields = form.Fields(IShibbolethLoginPortlet)
for name, field in schema.getFields(IShibbolethLoginPortlet).iteritems():
    if ITextLine.providedBy(field):
        form_fields[name].custom_widget = LongTextWidget

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.
class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form_fields

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form_fields
