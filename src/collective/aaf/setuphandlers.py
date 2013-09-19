from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


def setupVarious(context, site=None):
    """
    Set up various aspects of Plone that we can't set up using
    GenericSetup profiles (yet).  These aspects should be removed
        whenever possible and replaced with a GS import profile.
    """

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.aaf_various.txt') is None:
        return

    # Add additional setup code here
    site = site or getSite()

    # Manual install of AutoUserMakerPASPlugin
    qi = getToolByName(site, 'portal_quickinstaller')
    qi.installProduct('AutoUserMakerPASPlugin')

    # Configure the ACL plugin for auto user creation
    # This needs to be fully configurable via the web-based interface
    acl = getToolByName(site, 'acl_users')
    plugin = acl['AutoUserMakerPASPlugin']
    plugin.strip_domain_names = 0 #Domain name stripping
    plugin.http_remote_user = ('HTTP_AUEDUPERSONSHAREDTOKEN',
                               'HTTP_REMOTE_USER',)
    plugin.http_commonname = ('HTTP_DISPLAYNAME', 'HTTP_COMMONNAME')
    plugin.http_description = ()
    plugin.http_email = ('HTTP_EMAIL',)
    plugin.http_locality = ('HTTP_ORGANIZATIONNAME',)
    plugin.http_state = ()
    plugin.http_country = ()
    plugin.authzMappings = [
        {'groupid': [],
         'roles': {'Shibboleth Authenticated': 'on',
                   'Contributor': '',
                   'Editor': '',
                   'Manager': '',
                   'Owner': '',
                   'Reader': '',
                   'Reviewer': '',
                   'Site Administrator': ''},
         'userid': '',
         'values': {'HTTP_REMOTE_USER': ''},
         'version': 1
        }
    ]
