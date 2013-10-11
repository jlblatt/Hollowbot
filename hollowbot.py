###################################################################
# Hollowbot v1
# > Jason Blatt
############################################
# >> Email: jlblatt+hollowbot@gmail.com
# >> Git: https://github.com/jlblatt/Hollowbot
# >> See README and conf.py for more info
##########################

# TODO:
# - use data->after @ end of links to do multiple pages
# - use data->after @ end of comments to do full threads
# - setup reddit account and integrate api
# - cleanup _ conf variable
# - classes?

from sys import argv
from time import sleep

from conf import _

from init import db, cur
import log
import locations
import links
import comments
import stats

if len(argv) == 1 or 'cleanup' in argv:
    #Delete old links and comments
    if _['delete_links_after'] > -1: cur.execute("delete from t3 where created < date_sub(now(), interval %s second)", (_['delete_links_after'],))
    if _['delete_comments_after'] > -1: cur.execute("delete from t1 where created < date_sub(now(), interval %s second)", (_['delete_comments_after'],))
    db.commit();

# Build/store locations to retrieve links
if len(argv) == 1 or 'locations' in argv:
    locations.build(_['crawl_subreddits'], _['crawl_urls'])

# Crawls URLS from locations
if len(argv) == 1 or 'links' in argv:
    cur.execute("select id, url from crawl_locations where last_crawled < date_sub(now(), interval %s second)", (_['find_links_after'],))
    for l in cur.fetchall():
        links.get(l[1])
        cur.execute("update crawl_locations set last_crawled = now() where id = %s", (l[0],))
        db.commit()
        sleep(_['sleep'])

if len(argv) == 1 or 'comments' in argv:
    #Crawl eligible links
    cur.execute("select id, permalink from t3 where last_crawled < date_sub(now(), interval %s second)", (_['recrawl_links_after'],))
    for c in cur.fetchall():
        comments.get("http://www.reddit.com" + c[1] + ".json")
        cur.execute("update t3 set last_crawled = now() where id = %s", (c[0],))
        db.commit()
        sleep(_['sleep'])

stats.printStats()

if 'wipe' in argv:
    log.wipe()
    cur.execute("drop table if exists crawl_locations")
    cur.execute("drop table if exists t3")
    cur.execute("drop table if exists t1")
    db.commit()
    print "Data Wiped!!"

db.close()

if _['logging']: log.log.close()