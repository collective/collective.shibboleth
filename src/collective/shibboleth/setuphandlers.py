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

    if context.readDataFile('collective.shibboleth_various.txt') is None:
        return

    # Add additional setup code here
    site = site or getSite()

    # Manual install of AutoUserMakerPASPlugin
    qi = getToolByName(site, 'portal_quickinstaller')
    qi.installProduct('AutoUserMakerPASPlugin')
