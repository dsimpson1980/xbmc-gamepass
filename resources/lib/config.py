import ConfigParser
import os

config = ConfigParser.ConfigParser()
# default = os.path.expanduser('~/YahooFF/config')
default = os.path.join(os.path.dirname(__file__), '..', 'data', 'config')
config.read(default)

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
