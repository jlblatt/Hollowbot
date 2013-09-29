_ = dict()

_['name'] = "Hollowbot Clone"
_['version'] = "1.0a1"
_['description'] = "github clone of Hollowbot"
_['author'] = "Author Name"
_['author_url'] = "/user/xxx/"
_['author_email'] = "foo@bar.com"

_['db_host'] = "db_host"
_['db_name'] = "db_name"
_['db_user'] = "db_user"
_['db_pass'] = "db_pass"

_['logging'] = True
_['logtypes'] = ['exception', 'stat', 'message']
_['logfile'] = "log.txt"

_['crawl_urls'] = [
    "http://www.reddit.com/.json?limit=100"
]

# "Make no more than thirty requests per minute. 
#  This allows some burstiness to your requests, but keep it sane. 
#  On average, we should see no more than one request every two seconds from you."
#
#  https://github.com/reddit/reddit/wiki/API

_['timeout'] = 10

# Delete this next line to run
_['quit'] = True