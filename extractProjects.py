from pypodio2 import api
import json
import getpass
import ConfigParser
import sys


def user_input(prompt):
    '''
    Wrapper for raw_input with prompt text written to stderr
    @param prompt: Prompt to echo in terminal
    @type prompt: String
    '''
    sys.stderr.write(prompt)
    return raw_input()


def parseFields():
    '''
    TODO: write docstring
    '''



# Driver for extracting projects. Pulls all items from Podio project
# application and extracts key-value pairs matching external_id to
# value based on field_type.

# Get API credentials
config = ConfigParser.RawConfigParser()
config.read('key.cfg')
etl = config.get('APIKey', 'etl') # api app id
key = config.get('APIKey', 'key') # api key
app = config.get('APIKey', 'app') # podio internal app id

# Get user credentials
username = user_input('Username: ')
password = getpass.getpass('Password: ')

# Extract projects from Podio into dict
x = int(user_input('How many projects to pull?: '))
c = api.OAuthClient(etl, key, username, password)
projs = c.Application.get_items(app_id = app, limit = x)

# Map field ID to type in dictionary across projects
fields = dict()
for proj in projs['items']:
    for field in proj['fields']:
        fields[field['external_id']] = field['type']

# Print all field IDs and corresponding types
for f in fields:
    print "%s: %s" % (f, fields[f])

print fields.values()
