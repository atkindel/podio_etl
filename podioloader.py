
from pymysql_utils1 import MySQLDB
import getpass
from podioextractor import PodioExtractor

class PodioLoader(MySQLDB):
    '''
    Inherits MySQL interface from MySQLDB class; adds client method for
    loading Podio project data to local MySQL database.
    '''

    def __setupDB(self):
        '''
        Defines schema for project data and sets up database accordingly.
        '''
        # Build database if needed
        db.execute("CREATE DATABASE IF NOT EXISTS `Podio`;")

        # Drop pre-existing tables
        db.execute("DROP TABLE IF EXISTS `CourseIDMap`;")
        db.execute("DROP TABLE IF EXISTS `CourseVitals`;")
        db.execute("DROP TABLE IF EXISTS `CourseProduction`;")

        courseIDMap =   "CREATE TABLE `CourseIDMap` (" +\
                          "`course_display_name` varchar(50) DEFAULT NULL," +\
                          "`project_id` int(11) DEFAULT NULL" +\
                        ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"

        courseVitals =  "CREATE TABLE `CourseVitals` (" +\
                          "`project_id` int(11) DEFAULT NULL," +\
                          "`project_name` varchar(50) DEFAULT NULL," +\
                          "`school` varchar(50) DEFAULT NULL," +\
                          "`department` varchar(50) DEFAULT NULL," +\
                          "`institute` varchar(50) DEFAULT NULL," +\
                          "`faculty_name` varchar(50) DEFAULT NULL," +\
                          "`faculty_org` varchar(50) DEFAULT NULL," +\
                          "`faculty-title` varchar(50) DEFAULT NULL," +\
                          "`platform` varchar(50) DEFAULT NULL," +\
                          "`stanford-course` varchar(50) DEFAULT NULL," +\
                          "`quarter-offered` varchar(50) DEFAULT NULL," +\
                          "`duration` varchar(50) DEFAULT NULL," +\
                          "`exemplary-course3` varchar(50) DEFAULT NULL," +\
                          "`delivery-format` varchar(50) DEFAULT NULL," +\
                          "`course-type` varchar(50) DEFAULT NULL," +\
                          "`course-offering-type` varchar(50) DEFAULT NULL," +\
                          "`course-level` varchar(50) DEFAULT NULL" +\
                        ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"

        courseProd =    "CREATE TABLE `CourseProduction` (" +\
                          "`project_id` int(11) DEFAULT NULL," +\
                          "`vpol-priority` varchar(50) DEFAULT NULL," +\
                          "`engineering-support-level` varchar(50) DEFAULT NULL," +\
                          "`platform-support-level` varchar(50) DEFAULT NULL," +\
                          "`level-of-effort-id` varchar(50) DEFAULT NULL", +\
                          "`level-of-effort-production` varchar(50) DEFAULT NULL," +\
                          "`video-production-handling` varchar(50) DEFAULT NULL," +\
                          "`production-hours` varchar(50) DEFAULT NULL," +\
                          "`post-production-hours` varchar(50) DEFAULT NULL," +\
                          "`seed-grant` varchar(50) DEFAULT NULL," +\
                          "`funding-amount` int(11) DEFAULT NULL," +\
                          "`funding-source` varchar(50) DEFAULT NULL," +\
                          "`funding-stipulations` varchar(500) DEFAULT NULL" +\
                        ") ENGINE=MyISAM DEFAULT CHARSET=utf8;"

        db.execute(courseIDMap)
        db.execute(courseVitals)
        db.execute(courseProd)

    def __listify(self, iterable):
        '''
        Class method extends stringify list to return all entries in an
        iterable as a single string, comma delineated.
        '''
        iterlist = ''
        separator = ", "
        for item in iterable:
            iterlist += item + separator
        iterlist = iterlist[:-2] #remove extra separator
        iterlist = "(%s)" % iterlist #wrap in parens
        return iterlist

    def loadProjects(self, projects):
        '''
        Client method takes transformed project data and loads it according
        to the schema defined when the database is set up.
        '''
        self.__setupDB()
        for pid in projects:
            keys = self.listify(projects[pid].keys())
            values = self.listify(projects[pid].values())

            #TODO: split keys and values into two tables

            # build SQL query string
            query = "insert into q_IDMap(%s) values (%s);" % (keys, values)
            q_IDMap = "insert into "
            #TODO: include pid in each table!


# Initialize extractor from config file
extractor = PodioExtractor('key.cfg')

# Get user credentials for Podio and MySQL database
pd_user = extractor.user_input("Podio username: ")
pd_pass = getpass.getpass("Podio password: ")
db_user = extractor.user_input("MySQL username: ")
db_pass = getpass.getpass("MySQL password: ")

# Extract and transform Podio data to human-readable format
data = extractor.getProjects(username=pd_user, password=pd_pass)

# Load projects to MySQL database
db = PodioLoader(user=db_user, passwd=db_pass)
result = db.loadProjects(data)
db.close()
print result
