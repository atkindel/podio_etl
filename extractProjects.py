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

def parseFields(projects):
    '''
    Takes raw JSON-formatted projects from Podio and produces a dictionary
    mapping project IDs to a dictionaries of data fields for each project.
    @param projects: JSON-formatted string from Podio API
    @type projects: String
    '''
    data = dict()
    for proj in projects['items']:
        # Build fields dict
        fields = dict()
        fields['title'] = proj['title']
        for field in proj['fields']:
            ext_id = field['external_id']

            # type: category
            if field['type'] == "category":
                fields[ext_id] = field['values'][0]['value']['text']

            # type: text
            elif field['type'] == "text":
                #TODO: Scrub HTML from input
                fields[ext_id] = field['values'][0]['value']

            # type: contact
            elif field['type'] == "text":
                fields[ext_id + "-name"] = field['values'][0]['value']['name']
                fields[ext_id + "-title"] = field['values'][0]['value']['title']
                fields[ext_id + "-org"] = field['values'][0]['value']['organization']

            # type: duration
            elif field['type'] == "duration":
                fields[ext_id] = field['values'][0]['value']

            # type: embed
            elif field['type'] == "embed":
                #TODO: derive course DS-identifier from URLs
                continue

            # type: date
            elif field['type'] == "date":
                fields[ext_id] = field['values'][0]['start']

            # type: money
            elif field['type'] == "money":
                fields[ext_id] = field['values'][0]['value']

        # Map project uid to fields dict
        uid = proj['app_item_id']
        data[uid] = fields

    return data

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

# # Map field ID to type in dictionary across projects
# fields = dict()
# for proj in projs['items']:
#     for field in proj['fields']:
#         fields[field['external_id']] = field['type']
#
# # Print all field IDs and corresponding types
# for f in fields:
#     print "%s: %s" % (f, fields[f])
#
# print fields.values()
