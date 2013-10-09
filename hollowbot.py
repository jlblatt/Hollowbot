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
# - cleanup _ conf variable
# - change crawl URLs to subreddits
# - add command line args

from time import sleep

from conf import _

from init import db, cur
import log
import links
import comments
import stats

#Delete old links and comments
if _['delete_links_after'] > -1: cur.execute("delete from t3 where created < date_sub(now(), interval %s second)", (_['delete_links_after'],))
if _['delete_comments_after'] > -1: cur.execute("delete from t1 where created < date_sub(now(), interval %s second)", (_['delete_comments_after'],))
db.commit();

# Crawls URLS from datasources
for url in _['crawl_urls']:
    links.get(url)
    sleep(_['sleep'])

#Crawl eligible links
cur.execute("select id, permalink from t3 where last_crawled < date_sub(now(), interval %s second)", (_['recrawl_links_after'],))

for c in cur.fetchall():
    comments.get("http://www.reddit.com" + c[1] + ".json")
    cur.execute("update t3 set last_crawled = now() where id = %s", (c[0],))
    db.commit()
    sleep(_['sleep'])

stats.printStats()

db.close()
log.log.close()