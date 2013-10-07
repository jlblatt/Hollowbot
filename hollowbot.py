###################################################################
# Hollowbot v1
# > Jason Blatt
############################################
# >> Email: jlblatt+hollowbot@gmail.com
# >> Git: https://github.com/jlblatt/Hollowbot
# >> See README and conf.py for more info
##########################

# TODO:
# - use data->after @ end of getlinks.py to do multiple pages
# - setup reddit account and integrate api

from time import sleep

from conf import _

import log
from init import db, cur
import links
import comments
import timing

# Crawls URLS from datasources
for url in _['crawl_urls']:
    links.get(url)
    sleep(_['sleep'])

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