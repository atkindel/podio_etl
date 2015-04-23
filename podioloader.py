from pymysql_utils1 import MySQLDB
import getpass
from podioextractor import PodioExtractor

class PodioLoader(object):

    def __init__(self, username, password):
        self.db=MySQLDB('127.0.0.1', 3306, username, password, 'Podio')
        initDatabase()

    def loadProjects(data):
        #TODO: Implement this
        pass



# Get user credentials for Podio and MySQL database
pd_user = extractor.user_input("Podio username: ")
pd_pass = getpass.getpass("Podio password: ")
db_user = extractor.user_input("MySQL username: ")
db_pass = getpass.getpass("MySQL password: ")

# Fetch data from Podio and parse as needed
data = extractor.getProjects(username, password)

# Open database
db = PodioLoader(username, password)
db.loadProjects(data)
