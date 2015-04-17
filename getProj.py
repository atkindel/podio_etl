from pypodio2 import api
import json
import getpass
import ConfigParser

# Get API credentials
config = ConfigParser.RawConfigParser()
config.read('key.cfg')
etl = config.get('APIKey', 'etl') # api app id
key = config.get('APIKey', 'key') # api key
app = config.get('APIKey', 'app') # podio internal app id

# Get user credentials
username = raw_input('Username: ')
password = getpass.getpass('Password: ')

# Extract sample item for analysis
c = api.OAuthClient(etl, key, username, password)
s = c.Item.find(item_id = 36445119)

# Pretty print JSON output for review
spp = json.dumps(obj = s, sort_keys=True, indent = 4, separators = (',', ': '))
print spp;
