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

import datetime
import json
import MySQLdb
import re
import time
import urllib2
import warnings

warnings.filterwarnings('ignore', category = MySQLdb.Warning)

execfile('init.py')

# Crawls URLS from datasources
for url in _['crawl_urls']:
    getLinks(url)

#Delete old links
cur.execute("delete from t3 where created < date_sub(now(), interval %s second)", (_['delete_links_after']))
db.commit();

#Crawl eligible links
cur.execute("select id, permalink from t3 where last_crawled < date_sub(now(), interval %s second)", (_['recrawl_links_after'],))

for c in cur.fetchall():
    getComments("http://www.reddit.com" + c[1] + ".json")
    cur.execute("update t3 set last_crawled = now() where id = %s", (c[0],))
    db.commit()
    time.sleep(_['sleep'])

printStats()

db.close()
log.close()