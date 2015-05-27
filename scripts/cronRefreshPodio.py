from .podioextractor import PodioExtractor
from .podioloader import PodioLoader

# Read configuration file
cfg_dir = expanduser("~") + '/.ssh/key.cfg'
config = ConfigParser.RawConfigParser()
config.read(cfg_dir)

# Initialize extractor from config file
extractor = PodioExtractor(cfg_dir)

# Get user credentials for Podio and MySQL database
pd_user = config.get('PodioUser', 'p_user')
pd_pass = config.get('PodioUser', 'p_pass')
db_user = config.get('MySQLUser', 'm_user')
db_pass = config.get('MySQLUser', 'm_pass')

# Extract and transform Podio data to human-readable format
data = extractor.getProjects(username=pd_user, password=pd_pass)

# Load projects to MySQL database
db = PodioLoader(user=db_user, passwd=db_pass, db='Podio')
db.loadProjects(data)
db.close()
