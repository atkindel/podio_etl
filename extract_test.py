from podioextractor import PodioExtractor
import getpass
import json
import sys

### Test script for extracting projects from Podio.
# User provides login credentials and total # of projects to pull.

    # Initialize extractor
    extractor = PodioExtractor('key.cfg')

    # Get user input
    username = extractor.user_input('Username: ')
    password = getpass.getpass('Password: ')
    total = int(extractor.user_input('How many projects to pull?: '))

    # Using extractor, pull projects from Podio
    projects = extractor.getProjects(username, password, total)
    pp = json.dumps(obj=projects, sort_keys=True, indent=4)
    print pp
    sys.stderr.write("Successfully extracted %d projects.\n" % len(projects))
