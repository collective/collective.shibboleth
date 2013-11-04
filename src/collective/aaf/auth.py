import string
import random
from Products.statusmessages.interfaces import IStatusMessage

PW_CHARS = string.letters + string.digits

def _generatePassword(self):
    length = random.randint(24, 36)
    password = ''.join([random.choice(PW_CHARS) for i in xrange(length)])
    messages = IStatusMessage(self.REQUEST)
    messages.add(u"Your local account password is \"%s\" (excluding quotations). You should make a copy of this password in case you wish to access the site via WebDAV or other non-web methods. It will not be shown again, but can be changed via normal reset processes." % password, type=u"info")
    return password



