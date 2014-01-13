import json

try: confFile = open("conf.json", "r")
except Exception, e:
    print 'Error opening conf.json: %s'  % e
    exit(1)

confJSON = confFile.read()
confFile.close()

try: _ = json.loads(confJSON)
except Exception, e:
    print 'Error parsing conf.json (try http://jsonlint.com/): %s' % e
    exit(1)

# Check to make sure the user actually looked at the conf file
if 'quit' in _:
    print("Quit flag found in conf.json (you should probably at least look at the configuration before running, yeah?)")
    exit(1)

