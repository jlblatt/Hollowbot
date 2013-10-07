###################################################################
# Hollowbot v1
# > Jason Blatt
############################################
# >> Email: jlblatt+hollowbot@gmail.com
# >> Git: https://github.com/jlblatt/Hollowbot
# >> See README and conf.py for more info
##########################

# TODO:
# - move execfiles to modules
# - use data->after @ end of getlinks.py to do multiple pages
# - setup reddit account and integrate api
# - make conf JSON

from time import sleep

from conf import _

# Check to make sure the user actually looked at the conf file
if 'quit' in _:
    print("Quit flag found in conf.py (you should probably at least look at the configuration before running, yeah?)")
    exit(1)

from logging import printLog
from init import *

import links
import comments
import timing

# Crawls URLS from datasources
for url in _['crawl_urls']:
    links.get(url)

#Delete old links
cur.execute("delete from t3 where created < date_sub(now(), interval %s second)", (_['delete_links_after']))
db.commit();

#Crawl eligible links
cur.execute("select id, permalink from t3 where last_crawled < date_sub(now(), interval %s second)", (_['recrawl_links_after'],))

for c in cur.fetchall():
    comments.get("http://www.reddit.com" + c[1] + ".json")
    cur.execute("update t3 set last_crawled = now() where id = %s", (c[0],))
    db.commit()
    sleep(_['sleep'])

timing.printStats()

db.close()
log.close()