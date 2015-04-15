from pypodio2 import api
import json

username = input("Username: ")
password = input("Password: ")

c = api.OAuthClient(
    "podioetl",
    "bTirJmifPffG5swVMYDCdbnzIxDbw18TAEcT8qMCpUJxbvEb2O6aNQDVxqm8km18",
    username,
    password,
)

s = c.Item.find(265515261)

# Pretty print JSON output for review
spp = json.dumps(obj = s, sort_keys=True, indent = 4, separators = (',', ': '))
print spp;
