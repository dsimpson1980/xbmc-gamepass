import os

from resources.lib import yql
from resources.lib.yql.storage import FileTokenStore
import config


def get_y3():
    """Return an oauth connection from yql using consumer_key and
    consumer_secret that is either cached or requested from the user

    Parameters
    ----------
    None

    Returns
    -------
    yql.ThreeLegged
    """
    consumer_key, consumer_secret = config.get_consumer_secret()
    y3 = yql.ThreeLegged(consumer_key, consumer_secret, disable_ssl_certificate_validation=True)
    return y3

def get_token(y3, dialog=None):
    """Check if there is a cached token and if so retrieve it else ask the user
    for a new token using dialog.

    The cached token is stored in ~/YahooFF/

    Parameters
    ----------
    y3:
    dialog:

    Returns
    -------
    yql.YahooToken
        Either the cached token or a newly requested token
    """
    _cache_dir = os.path.expanduser('~/YahooFF')
    if not os.access(_cache_dir, os.R_OK):
        os.mkdir(_cache_dir)
    token_store = FileTokenStore(_cache_dir, secret='sasfasdfdasfdaf')
    stored_token = token_store.get('foo')
    if not stored_token:
        request_token, auth_url = y3.get_token_and_auth_url()
        if dialog is not None:
            verifier = dialog(auth_url)
        else:
            print "Visit url %s and get a verifier string" % auth_url
            verifier = raw_input("Enter the code: ")
        token = y3.get_access_token(request_token, verifier)
        token_store.set('foo', token)
    else:
        token = y3.check_token(stored_token)
        if token != stored_token:
            token_store.set('foo', token)
    return token
