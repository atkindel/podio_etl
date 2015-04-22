from podioextractor import PodioExtractor
import getpass
import json
import sys

### Script for extracting project fields from Podio.
# User provides login credentials and total # of projects to pull.
# Prints a list of fields with examples for schema analysis.

# Initialize extractor
extractor = PodioExtractor('key.cfg')

# Get user input
username = extractor.user_input('Username: ')
password = getpass.getpass('Password: ')
total = int(extractor.user_input('How many projects to pull?: '))

# Using extractor, pull projects from Podio
projects = extractor.getProjects(username, password, total)
pp = json.dumps(obj=projects, sort_keys=True, indent=4)
sys.stderr.write("Successfully extracted %d projects.\n" % len(projects))

# Get all fields
fields = dict()
for pid in projects:
    fields["project_id"] = pid
    fields.update(projects[pid])
pp = json.dumps(obj=fields, sort_keys=True, indent=4)
print pp
