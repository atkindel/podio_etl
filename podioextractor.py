from pypodio2 import api
import json
import getpass
import ConfigParser
from urlparse import urlparse
import sys


class PodioExtractor(object):
    '''
    Interface to Podio API for extracting project information.
    '''
    def __init__(self, config):
        '''
        @param config: .cfg file with api config info
        @type config: String
        '''
        try:
            config = ConfigParser.RawConfigParser()
            config.read('key.cfg')
            self.etl = config.get('APIKey', 'etl') # api app id
            self.key = config.get('APIKey', 'key') # api key
            self.app = config.get('APIKey', 'app') # podio internal app id
        except IOError:
            print ("File %s not found." % config)

    def user_input(self, prompt):
        '''
        Wrapper for raw_input with prompt written to stderr. Useful for piping
        stdout to file from command line, e.g. when reviewing JSON output.

        @param prompt: Prompt to echo in terminal
        @type prompt: String
        '''
        sys.stderr.write(prompt)
        return raw_input()

    def parseCourseURL(self, url):
        '''
        Derives database identifiers from URLs.

        @param url: Platform URL
        @type url: String
        '''
        purl = urlparse(url)
        return purl.path

    def transformProjects(self, projects):
        '''
        Takes raw JSON-formatted projects from Podio and produces a dictionary
        mapping project IDs to a dictionary of data fields for each project.

        @param projects: JSON-formatted string from Podio API
        @type projects: String
        '''
        #TODO: Document output into SQL schema

        projectData = dict()
        for proj in projects['items']:
            # Build fields dict, initialize with course title
            fieldData = { 'title': proj['title'] }
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
                    url = field['values'][0]['embed']['original_url']
                    fieldData[ext_id] = url

                    # parse db internal id for course if correct URL
                    if ext_id == 'course-url':
                        fieldData['course_display_name'] = self.parseCourseURL(url)

                # type: date
                elif field['type'] == "date":
                    fieldData[ext_id] = field['values'][0]['start']

                # type: money
                elif field['type'] == "money":
                    fieldData[ext_id] = field['values'][0]['value']

                # type: progress (not used here)
                elif field['type'] == "progress":
                    pass

            # Finally, map project uid to built fields dict
            uid = proj['app_item_id']
            projectData[uid] = fieldData

        return projectData

    def extractProjects(self, username, password, num_projs):
        '''
        Given user login information, return JSON-formatted projects.

        @param username: Username for Podio account (usually an email address)
        @type username: String
        @param password: Password for Podio account
        @type password: String
        @param num_projs:
        @type num_projs:
        '''
        #TODO: Currently limited to pulling 500 projects at once.
        c = api.OAuthClient(self.etl, self.key, username, password)
        projects = c.Application.get_items(app_id = self.app, limit = num_projs)
        return projects



# Driver for extracting projects when module called from command line. Pulls all
# items from Podio project application and extracts key-value pairs matching
# external_id to value based on field_type. Requires correct config file and
# appropriate user credentials on Podio to work correctly.

if __name__ == '__main__':

    # Initialize extractor
    extractor = PodioExtractor('key.cfg')

    # Get credentials from user
    username = extractor.user_input('Username: ')
    password = getpass.getpass('Password: ')

    # Using extractor, pull projects from Podio
    total = int(extractor.user_input('How many projects to pull?: '))
    projs = extractor.extractProjects(username, password, total)

    # Output project JSON (pretty-printed)
    pp_projs = json.dumps(obj=projs, sort_keys=True, indent=4, separators=(',', ': '))
    print(pp_projs)

    # Transform extracted projects
    parsed_projs = extractor.transformProjects(projs)
