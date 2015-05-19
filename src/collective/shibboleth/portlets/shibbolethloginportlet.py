import json
import re
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.schema.interfaces import ITextLine
from zope.formlib import form
from zope.formlib.textwidgets import TextWidget
from Products.CMFCore.Expression import createExprContext, Expression
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.shibboleth import shibbolethMessageFactory as _

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
    """ Login portlet for Shibboleth EDS

    Mandatory default settings have not been included as they require
    changes to the CSS and language settings have been excluded also.

    It inherits from IPortletDataProvider because for this portlet, the data
    that is being rendered and the portlet assignment itself are the same.
    """
    header = schema.TextLine(
        title=__(u"Portlet header"),
        description=__(u"Title of the rendered portlet"),
        constraint=re.compile("[^\s]").match,
        default=_(u"Institutional Login"),
        required=True
    )
    sp_handlerURL = TALESTextLine(
        title=_(u"Service Provider Handler URL (TALES)"),
        description=_(u"URL of the Shibboleth handler for the given "
                      u"Service Provider (SP) responder."),
        default=u"string:${portal_url}/Shibboleth.sso",
        required=False
    )
    eds_alwaysShow = schema.Bool(
        title=_(u"Always show results"),
        description=_(u"If true, results will be shown as soon as you start "
                      u"typing."),
        default=True,
        required=False
    )
    # Intentially set as the portal_url as the default
    eds_dataSource = TALESTextLine(
        title=_(u"Data source (TALES)"),
        description=_(u"URL of your JSON Shibboleth Discovery Feed."),
        default=u"string:${portal_url}/Shibboleth.sso/DiscoFeed",
        required=True
    )
    eds_defaultLanguage = TALESTextLine(
        title=_(u"Default language (TALES)"),
        description=_(u"Language to use if the browser's language isn't "
                      u"supported by the EDS. Defaults to the current Plone "
                      u"language."),
        default=u"string:${context/@@plone_portal_state/language}",
        required=False
    )
    eds_defaultLogo = TALESTextLine(
        title=_(u"Default logo (TALES)"),
        description=_(u"Default logo to show for Identity Providers listed."),
        default=u"string:${context/@@plone_portal_state/navigation_root_url}/++resource++shibboleth-ds/blank.gif",
        required=False
    )
    eds_defaultLogoWidth = schema.Int(
        title=_(u"Default logo width"),
        description=_(u"Width of default logo in pixels."),
        default=1,
        required=False
    )
    eds_defaultLogoHeight = schema.Int(
        title=_(u"Default logo height"),
        description=_(u"Height of default logo in pixels."),
        default=1,
        required=False
    )
    eds_defaultReturn = TALESTextLine(
        title=_(u"Default return URL (TALES)"),
        description=_(
            u"URL to send users who login via the EDS interface. "
            u"This portlet generates a dynamic return URL by default "
            u"which handles return URLs and query strings."),
        default=u"string:${view/login_url}",
        required=True
    )
    eds_defaultReturnIDParam = TALESTextLine(
        title=_(u"Default return ID parameters (TALES)"),
        required=False
    )
    eds_helpURL = TALESTextLine(
        title=_(u"Help URL (TALES)"),
        default=u"string:https://wiki.shibboleth.net/confluence/display/EDS10",
        required=False
    )
    eds_ie6Hack = schema.List(
        title=_(u"IE 6 hack"),
        description=_(
            u"An array of structures to disable when drawing the pull down "
            u"(needed to handle the ie6 z axis problem)."),
        value_type=schema.TextLine(),
        required=False,
    )
    eds_insertAtDiv = schema.TextLine(
        title=_(u"Insertion element ID"),
        description=_(u"The div element ID where the EDS will be inserted."),
        default=u"idpSelect",
        required=True
    )
    eds_maxResults = schema.Int(
        title=_(u"Maximum results"),
        description=_(u"Number of results to show at once or the number at "
                      u"which to start showing if alwaysShow is false."),
        default=10,
        required=True
    )
    eds_myEntityID = TALESTextLine(
        title=_(u"Entity ID (TALES)"),
        description=_(u"If specified, this must match the string provided in "
                      u"the Discovery Service (DS) parameters."),
        default=None,
        required=False
    )
    eds_preferredIdP = schema.List(
        title=_(u"Preferred identity providers"),
        description=_(u"List of entity IDs to always show as preferred "
                      u"organisations."),
        value_type=schema.TextLine(),
        required=False,
    )
    eds_hiddenIdP = schema.List(
        title=_(u"Hidden identity providers"),
        description=_(u"List of entity IDs to always hide from the list of "
                      u"preferred organisations."),
        value_type=schema.TextLine(),
        required=False,
    )
    eds_ignoreKeywords = schema.Bool(
        title=_(u"Ignore keywords"),
        description=_(u"If true, ignore the mdui:Keywords tag when looking "
                      u"for candidates."),
        default=False,
        required=False
    )
    eds_showListFirst = schema.Bool(
        title=_(u"Show list first"),
        description=_(u"If true, start with a drop-down list of IdPs."),
        default=False,
        required=False
    )
    eds_samlIdPCookieTTL = schema.Int(
        title=_(u"IdP cookie expiration time"),
        description=_(u"How long to remember identity providers (in days)."),
        default=730,
        required=False
    )
    eds_setFocusTextBox = schema.Bool(
        title=_(u"Initial focus on text box"),
        description=_(u"If not set, initial focus will be supressed."),
        default=True,
        required=False
    )
    eds_testGUI = schema.Bool(
        title=_(u"Enable test GUI"),
        default=False,
        required=False
    )
    eds_doNotCollapse = schema.Bool(
        title=_(u"Always show logos"),
        description=_(u"If not set, default logos will be hidden if "
                      u"none of the preferred Identity Providers have a "
                      u"logo."),
        default=True,
        required=False
    )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IShibbolethLoginPortlet)

    header = _(u"Institutional Login")
    sp_handlerURL = u"string:${portal_url}/Shibboleth.sso"
    eds_alwaysShow = True
    eds_dataSource = u"string:${portal_url}/Shibboleth.sso/DiscoFeed"
    eds_defaultLanguage = u"string:${context/@@plone_portal_state/language}"
    eds_defaultLogo = u"string:${context/@@plone_portal_state/navigation_root_url}/++resource++shibboleth-ds/blank.gif"
    eds_defaultLogoWidth = 1
    eds_defaultLogoHeight = 1
    eds_defaultReturn = u"string:${view/login_url}"
    eds_defaultReturnIDParam = None
    eds_helpURL = u"string:https://wiki.shibboleth.net/confluence/display/EDS10"
    eds_ie6Hack = None
    eds_insertAtDiv = u"idpSelect"
    eds_maxResults = 10
    eds_myEntityID = None
    eds_preferredIdP = None
    eds_hiddenIdP = None
    eds_ignoreKeywords = False
    eds_showListFirst = False
    eds_samlIdPCookieTTL = 730
    eds_setFocusTextBox = True
    eds_testGUI = False
    eds_doNotCollapse = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # List default arguments
        for arg in ('eds_ie6Hack', 'eds_preferredIdP', 'eds_hiddenIdP'):
            if kwargs.get(arg) is None:
                setattr(self, arg, [])

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header


def execute_expression(expr, folder, portal, context=None, **kwargs):
    """ Execute and expand a given TALES `expr`.

    Because the way in which portlets are rendered, the context needs
    to be corrected to be the surrounding folder.

    Also accepts arbitrary kwargs and applies them into the expression
    context for execution.
    """
    ec = createExprContext(folder, portal, context)
    ec.contexts['context'] = ec.contexts['here']
    ec.vars['context'] = ec.vars['here']
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
                                  folder=self.context,
                                  portal=self.portal,
                                  context=self.context,
                                  view=self)

    def login_url(self):
        """ Generate a suitable login URL for non-JavaScript users.

        The final ``target`` in the URL will be where the user is
        redirected to from Shibboleth.
        """
        return self._execute_expression(self.data.sp_handlerURL) \
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
                self.request.QUERY_STRING = \
                    self.request.QUERY_STRING.replace('/logged_out', '')
            url += '?' + self.request.QUERY_STRING
        return url

    def embedded_ds_options(self):
        """ Generate JSON configuration for the Embedded Discovery Service.

        Interpolates the TALES fields with the relevant values to produce
        suitable output variables for configuration.
        """
        # Ignore URL params by default for Plone Not Authorized redirects
        options = {'ignoreURLParams': True}
        for name, field in \
            schema.getFields(IShibbolethLoginPortlet).iteritems():
            if name.startswith('eds_'):
                value = getattr(self.data, name)
                if value and ITALESTextLine.providedBy(field):
                    value = self._execute_expression(value)
                options[name[4:]] = value

        return json.dumps(options)


# Customise field display length
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
