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

def parseCourseURL(url):
    '''
    Derives database identifiers from URLs.
    @param url: Platform URL
    @type url: String
    '''
    out = ''
    # if https://class.stanford.edu/courses/English/10poems/Spring2015/about -> English/10poems/Spring2015
    if ("stanford.edu" in url):
        head = #35 for class.stanford.edu, but not for lagunita... what to do here?
        trail = url.find("/about")
        out = url[head:trail]
    elif ("coursera.org" in url):
        #TODO: parse Cera URLs
    elif ("novoed.com" in url):
        #TODO: parse Ned URLs
    else
        out = "N/A"

    return out

def parseFields(projects):
    '''
    Takes raw JSON-formatted projects from Podio and produces a dictionary
    mapping project IDs to a dictionary of data fields for each project.
    @param projects: JSON-formatted string from Podio API
    @type projects: String
    '''
    #TODO: document fields not ingested and rationale
    #TODO: document this schema

    projectData = dict()
    for proj in projects['items']:
        # Build fields dict, initialize by
        fieldData = dict('title': proj['title'])
        for field in proj['fields']:
            ext_id = field['external_id']

            # type: category
            if field['type'] == "category":
                fieldData[ext_id] = field['values'][0]['value']['text']

            # type: text
            elif field['type'] == "text":
                #TODO: Scrub HTML from input
                fieldData[ext_id] = field['values'][0]['value']

            # type: contact
            elif field['type'] == "text":
                fieldData[ext_id + "-name"] = field['values'][0]['value']['name']
                fieldData[ext_id + "-title"] = field['values'][0]['value']['title']
                fieldData[ext_id + "-org"] = field['values'][0]['value']['organization']

            # type: duration
            elif field['type'] == "duration":
                fieldData[ext_id] = field['values'][0]['value']

            # type: embed
            elif field['type'] == "embed":
                #TODO: derive course DS-identifier from URLs
                pass

            # type: date
            elif field['type'] == "date":
                fieldData[ext_id] = field['values'][0]['start']

            # type: money
            elif field['type'] == "money":
                fieldData[ext_id] = field['values'][0]['value']

            # type: progress (not used here)
            elif field['type'] == "progress":
                pass

        # Map project uid to fields dict
        uid = proj['app_item_id']
        projectData[uid] = fieldData

    return projectData



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

# Extract JSON-formatted project data from Podio
x = int(user_input('How many projects to pull?: '))
c = api.OAuthClient(etl, key, username, password)
projs = c.Application.get_items(app_id = app, limit = x)

# Process raw JSON into dictionary of projects
# TODO: call parseFields on projs, test output
