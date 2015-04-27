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
        self.execute("CREATE DATABASE IF NOT EXISTS `Podio`;")

        # Drop pre-existing tables
        self.execute("DROP TABLE IF EXISTS `CourseIDMap`;")
        self.execute("DROP TABLE IF EXISTS `CourseVitals`;")
        self.execute("DROP TABLE IF EXISTS `CourseProduction`;")

        courseIDMap = (
                        """
                        CREATE TABLE `CourseIDMap` (
                        `project-id` varchar(50) DEFAULT NULL,
                        `course-display-name` varchar(500) DEFAULT NULL
                        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
                        """
        )

        courseVitals = (
                        """
                        CREATE TABLE `CourseVitals` (
                        `project-id` int(11) DEFAULT NULL,
                        `project-name` varchar(500) DEFAULT NULL,
                        `school` varchar(50) DEFAULT NULL,
                        `department` varchar(50) DEFAULT NULL,
                        `institute` varchar(50) DEFAULT NULL,
                        `faculty-name` varchar(50) DEFAULT NULL,
                        `faculty-org` varchar(200) DEFAULT NULL,
                        `faculty-title` varchar(200) DEFAULT NULL,
                        `platform` varchar(50) DEFAULT NULL,
                        `stanford-course` varchar(50) DEFAULT NULL,
                        `quarter-offered` varchar(50) DEFAULT NULL,
                        `duration` varchar(50) DEFAULT NULL,
                        `exemplary-course3` varchar(50) DEFAULT NULL,
                        `delivery-format` varchar(50) DEFAULT NULL,
                        `course-type` varchar(50) DEFAULT NULL,
                        `course-offering-type` varchar(50) DEFAULT NULL,
                        `course-level` varchar(50) DEFAULT NULL
                        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
                        """
        )

        courseProd = (
                        """
                        CREATE TABLE `CourseProduction` (
                        `project-id` int(11) DEFAULT NULL,
                        `vpol-priority` varchar(50) DEFAULT NULL,
                        `engineering-support-level` varchar(50) DEFAULT NULL,
                        `platform-support-level` varchar(50) DEFAULT NULL,
                        `level-of-effort-id` varchar(50) DEFAULT NULL,
                        `level-of-effort-production` varchar(50) DEFAULT NULL,
                        `video-production-handling` varchar(50) DEFAULT NULL,
                        `production-hours` varchar(50) DEFAULT NULL,
                        `post-production-hours` varchar(50) DEFAULT NULL,
                        `seed-grant` varchar(50) DEFAULT NULL,
                        `funding-amount` int(11) DEFAULT NULL,
                        `funding-source` varchar(50) DEFAULT NULL,
                        `funding-stipulations` varchar(2000) DEFAULT NULL
                        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
                        """
        )

        self.execute(courseIDMap)
        self.execute(courseVitals)
        self.execute(courseProd)

    def __listify(self, iterable, cols=False):
        '''
        Given an iterable, returns all entries in the iterable as a
        single string, comma delineated. Cols should be set to true if
        iterable being listified contains column names for MySQL table.
        '''
        iterlist = ''
        separator = ", "
        for item in iterable:
            if cols:
                item = "`%s`" % item
            iterlist += '%s' % item + separator
        iterlist = iterlist[:-2] #remove extra separator
        return iterlist

    def __schema(self, table):
        '''
        Given a table name, return a list of column names in the table.
        '''
        qstr = "SHOW COLUMNS FROM %s" % table
        qiter = self.query(qstr)
        schema = []
        for q in qiter:
            schema.append(q[0])
        return schema

    def __loadTable(self, projects, table):
        '''
        Iterates through projects dict and grabs values that match column names
        in the specified table. Then, executes a query to insert data for each
        project in the dict into the specified table.
        '''

        for pid in projects:
            # Use only relevant fields for this specific table and project
            schema = self.__schema(table)
            fields = projects[pid].keys()
            columns = set(schema).intersection(fields)

            # Get data from this project
            data = dict()
            for column in columns:
                value = projects[pid][column]
                data[column] = '"%s"' % value

            # Build and run query
            keys = self.__listify(data.keys(), True)
            values = self.__listify(data.values())
            query = "INSERT INTO %s(%s) VALUES (%s);" % (table, keys, values)
            self.execute(query.encode('UTF_8', 'ignore'))

    def loadProjects(self, projects):
        '''
        Client method takes transformed project data and loads it according
        to the schema defined when the database is set up.
        '''
        self.__setupDB()
        total = len(projects)
        self.__loadTable(projects, "CourseIDMap")
        print "CourseIDMap loaded with data from %d projects.\n" % total
        self.__loadTable(projects, "CourseVitals")
        print "CourseVitals loaded with data from %d projects.\n" % total
        self.__loadTable(projects, "CourseProduction")
        print "CourseProduction loaded with data from %d projects.\n" % total



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
db = PodioLoader(user=db_user, passwd=db_pass, db='Podio')
db.loadProjects(data)
db.close()
