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
# - add timing code to determine if/when to crawl
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

START_TIME = time.time()
LINK_TIMES = {'counts' : [] , 'times' : []}
COMMENT_TIMES = {'counts' : [] , 'times' : []}

execfile('init.py')

for url in _['crawl_urls']:
    getLinks(url)

cur.execute("select id, permalink from t3")

for c in cur.fetchall():
    time.sleep(_['timeout'])
    getComments("http://www.reddit.com" + c[1] + ".json")
    cur.execute("update t3 set last_crawled = now() where id = %s", (c[0],))
    db.commit()

printlog(str(sum(LINK_TIMES['counts'])) + " links / " + str(sum(LINK_TIMES['times'])) + " sec. (" + str(sum(LINK_TIMES['times']) / sum(LINK_TIMES['counts'])) + " sec. ea.) in " + str(len(LINK_TIMES['counts'])) + " locations", 'stat')
printlog(str(sum(COMMENT_TIMES['counts'])) + " comments / " + str(sum(COMMENT_TIMES['times'])) + " sec. (" + str(sum(COMMENT_TIMES['times']) / sum(COMMENT_TIMES['counts'])) + " sec. ea.) in " + str(len(COMMENT_TIMES['counts'])) + " locations", 'stat')

printlog("Done! (execution took " + str(time.time() - START_TIME) + " sec.)", 'message')
db.close()
log.close()