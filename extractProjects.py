from pypodio2 import api
import json
import getpass
import ConfigParser
import readline

# Get API credentials
config = ConfigParser.RawConfigParser()
config.read('key.cfg')
app = config.get('APIKey', 'app')
key = config.get('APIKey', 'key')

# Get user credentials
username = raw_input('Username: ')
password = getpass.getpass('Password: ')

# Pull X projects from Podio
x = 25
c = api.OAuthClient(app, key, username, password)
dict = c.Application.get_items(app_id = 2589515, limit = x)

# Pretty print JSON output for review
dictpp = json.dumps(obj = dict, sort_keys=True, indent = 4, separators = (',', ': '))
print dictpp
