from pypodio2 import api
import json
import getpass
import ConfigParser
from urlparse import urlparse
import sys


class PodioExtractor(object):
    '''
    Interface to Podio API for extracting project information.
    Author: Alex Kindel
    '''
    def __init__(self, config):
        '''
        Initialize with a config file.

        @param config: .cfg file with api config info. Expected format as follows:
        [APIKey]
        etl=<Podio client ID>
        key=<Podio client secret>
        app=<Podio app number>
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

    def __cleanQuotes(self, text):
        '''
        Eliminates quote marks from a given string.
        '''
        return text.replace('"', '').replace("'", "")

    def __parseCourseURL(self, url):
        '''
        Derives database identifiers from URLs.

        @param url: Platform URL
        @type url: String
        '''
        cid = urlparse(url).path
        if 'stanford.edu' in url:
            cid = cid[8:-5] # remove extra info from SU URLs
        cid = cid.strip('/')
        return cid

    def __transformBatch(self, projects):
        '''
        Takes raw projects from Podio and produces a dictionary mapping project
        IDs to a dictionary of data fields for each project.

        @param projects: Raw dict of projects out of Podio API
        @type projects: Dictionary
        '''

        projectData = dict()
        for proj in projects['items']:
            # Build fields dict, initialize with course title and project id
            fieldData = { 'title': proj['title'], 'project-id': proj['app_item_id'] }
            for field in proj['fields']:
                ext_id = field['external_id']

                try:
                    # type: category
                    if field['type'] == "category":
                        fieldData[ext_id] = field['values'][0]['value']['text']

                    # type: text
                    elif field['type'] == "text":
                        text = field['values'][0]['value']
                        text = self.__cleanQuotes(text)
                        fieldData[ext_id] = text

                    # type: contact
                    elif field['type'] == "contact":
                        fieldData[ext_id + "-name"] = field['values'][0]['value']['name']
                        fieldData[ext_id + "-title"] = field['values'][0]['value']['title'][0]
                        fieldData[ext_id + "-org"] = field['values'][0]['value']['organization']

                    # type: duration
                    elif field['type'] == "duration":
                        fieldData[ext_id] = field['values'][0]['value']

                    # type: embed
                    elif field['type'] == "embed":
                        url = field['values'][0]['embed']['original_url']
                        url = self.__cleanQuotes(url) #remove extraneous quotation marks
                        fieldData[ext_id] = url

                        # parse db-internal id for course if correct URL
                        if ext_id == 'course-url':
                            fieldData['course-display-name'] = self.__parseCourseURL(url)

                    # type: date
                    elif field['type'] == "date":
                        fieldData[ext_id] = field['values'][0]['start']

                    # type: money
                    elif field['type'] == "money":
                        fieldData[ext_id] = field['values'][0]['value']

                    # type: progress (not used here)
                    elif field['type'] == "progress":
                        pass
                except KeyError:
                    pass

            # Finally, map project uid to built fields dict
            uid = proj['app_item_id']
            projectData[uid] = fieldData

        return projectData

    def __extractBatch(self, username, password, batch_size, off):
        '''
        Given user login information, return dict of projects.

        @param username: Username for Podio account (usually an email address)
        @type username: String
        @param password: Password for Podio account
        @type password: String
        @param batch_size: Number of projects to pull in this batch
        @type batch_size: Integer
        '''
        c = api.OAuthClient(self.etl, self.key, username, password)
        projects = c.Application.get_items(app_id = self.app, limit = batch_size, offset = off)
        return projects

    def getProjects(self, username, password, total=2000):
        '''
        Primary client method. In batches of up to 500 projects, extracts
        projects and parses project data into intermediate representation.
        Returns dictionary matching project IDs to projects, which are
        themselves represented as dicts of field IDs to field values.

        @param username: Username for Podio account (usually an email address)
        @type username: String
        @param password: Password for Podio account
        @type password: String
        @param num_projs: Total number of projects to pull
        @type num_projs: Integer
        '''
        projects = dict()
        batch_size = total if total<=500 else 500
        off = 0
        while off < total:
            batch = self.__extractBatch(username, password, batch_size, off)
            parsed = self.__transformBatch(batch)
            projects.update(parsed)
            off += batch_size
        return projects


# Driver for extracting projects when module called from command line. Pulls all
# items from Podio project application and extracts key-value pairs matching
# external_id to value based on field_type. Requires correct config file and
# appropriate user credentials on Podio to work correctly. Pulls all projects by
# default, but module allows client script to decide how many projects pulled.

if __name__ == '__main__':

    # Initialize extractor
    extractor = PodioExtractor('key.cfg')

    # Get user input
    username = extractor.user_input('Username: ')
    password = getpass.getpass('Password: ')

    # Using extractor, pull projects from Podio
    projects = extractor.getProjects(username, password)
    pp = json.dumps(obj=projects, sort_keys=True, indent=4)
    print pp
    sys.stderr.write("Successfully extracted %d projects.\n" % len(projects))
