_ = dict()

# https://github.com/reddit/reddit/wiki/API
#
# We're happy to have API clients, crawlers, scrapers, and Greasemonkey scripts, but they have to obey some rules:
#
#   Make no more than thirty requests per minute. This allows some burstiness to your requests, but keep it sane. On average, we should see no more than one request every two seconds from you.
#   Change your client's User-Agent string to something unique and descriptive, preferably referencing your reddit username.
#        Example: User-Agent: flairbot/1.0 by spladug
#        Many default User-Agents (like "Python/urllib" or "Java") are drastically limited to encourage unique and descriptive user-agent strings.
#        If you're making an application for others to use, please include a version number in the user agent. This allows us to block buggy versions without blocking all versions of your app.
#        NEVER lie about your user-agent. This includes spoofing popular browsers and spoofing other bots. We will ban liars with extreme prejudice.
#    Most pages are cached for 30 seconds, so you won't get fresh data if you request the same page that often. Don't hit the same page more than once per 30 seconds.
#    Requests for multiple resources at a time are always better than requests for single-resources in a loop. Talk to us on the mailing list or in #reddit-dev if we don't have a batch API for what you're trying to do.
#    Our robots.txt is for search engines not API clients. Obey these rules for API clients instead.
#
# https://github.com/reddit/reddit/wiki/API

#Name/Author
_['name'] = "Hollowbot Clone"
_['version'] = "1.0a1"
_['description'] = "github clone of Hollowbot"
_['author'] = "Author Name"
_['author_url'] = "/user/xxx/"
_['author_email'] = "foo@bar.com"

#Database
_['db_host'] = "db_host"
_['db_name'] = "db_name"
_['db_user'] = "db_user"
_['db_pass'] = "db_pass"

#Logging
_['logging'] = True
_['logtypes'] = ['exception', 'error', 'stat', 'message']
_['logfile'] = "log.txt"

#Crawl Rules
_['crawl_urls'] = [
    "http://www.reddit.com/.json?limit=100"
]
_['recrawl_links_after'] = 60 * 60 # seconds
_['delete_links_after'] = 60 * 60 * 24 # seconds

_['sleep'] = 10 # seconds



# Delete this next line to run
_['quit'] = True