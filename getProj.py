from pypodio2 import api
import json
import getpass
import ConfigParser

# Get API credentials
config = ConfigParser.RawConfigParser()
config.read('key.cfg')
app = config.get('APIKey', 'app')
key = config.get('APIKey', 'key')

# Get user credentials
username = raw_input("Username: ")
password = getpass.getpass("Password: ")

# Extract sample item for analysis
c = api.OAuthClient(app, key, username, password)
s = c.Item.find(265515261)

# Pretty print JSON output for review
spp = json.dumps(obj = s, sort_keys=True, indent = 4, separators = (',', ': '))
print spp;
