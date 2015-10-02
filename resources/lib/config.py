import ConfigParser
import os
import errno
import shutil

config = ConfigParser.ConfigParser()
default = os.path.expanduser('~/YahooFF/config')

def set_default_config():
    mkdir_p('~/YahooFF')
    src = os.path.join(os.path.dirname(__file__), 'default_config')
    dst = os.path.expanduser('~/YahooFF/config')
    shutil.copy(src, dst)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def config_map(section, key):
    try:
        value = config.get(section, key)
        if value == '':
            value = raw_input('Enter %s %s:' % (section, key))
            config.set(section, key, value)
        with open(default, 'w') as f:
            config.write(f)
    except ConfigParser.NoOptionError:
        value = None
    return value

def get_consumer_secret(query=None):
    consumer = config_map('Yff', 'consumer')
    secret = config_map('Yff', 'secret')
    if '' in [consumer, secret]:
        if query is None:
            consumer = raw_input('Enter %s:' % 'consumer')
            secret = raw_input('Enter %s:' % 'secret')
        else:
            consumer, secret = query()
    return consumer, secret

def get_yahoo_username(query=None):
    """Get the yahoo username from the config file

    Parameters
    ----------
    query: function
        A function returning the parameter if it does not exist in the config
        file

    Returns
    -------
    str
        The yahoo_username to use to login for scraping projected points
    """
    return get_general_one_parameter(query, 'Yahoo', 'username')

def get_gui_parameter(query=None):
    """Fetch a parameter associated with the gui e.g. refresh_rate

    Parameters
    ----------
    query: function
        A function that returns the value for the parameter if it doesn't exist

    Returns
    -------
    int
        The refresh rate for loading player_points in milliseconds
    """
    return int(get_general_one_parameter(query, 'Parameters', 'refresh_rate'))

def get_league(query=None):
    return get_general_one_parameter(query, 'Fantasy', 'league')

def get_league_number(query=None):
    return get_general_one_parameter(query, 'Fantasy', 'league_number')

def get_league_key():
    return '%s.l.%s' % (get_league(), get_league_number())

def get_general_one_parameter(query, section, key):
    value = config_map(section, key)
    if value == '':
        value = raw_input('Enter %s:' % key) if query is None else query()
    return value

if not os.path.exists(default):
    set_default_config()
config.read(default)
