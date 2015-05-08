import cgi
import json

def escape_javascript(value):
    """ Escape any potential JavaScript or HTML from untrusted sources.
    """
    return cgi.escape(json.dumps(value))

