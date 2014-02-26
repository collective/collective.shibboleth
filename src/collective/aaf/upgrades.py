from Products.CMFPlone.utils import getToolByName

PROFILE_ID = 'profile-collective.aaf:default'


def upgrade_0001_to_0002(context):
    acl = getToolByName(context, 'acl_users')
    plugin = acl['AutoUserMakerPASPlugin']
    plugin.auto_update_user_properties = 1

