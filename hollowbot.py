###################################################################
# Hollowbot v1
# > Jason Blatt
############################################
# >> Email: jlblatt+hollowbot@gmail.com
# >> Git: https://github.com/jlblatt/Hollowbot
# >> See README and conf.py for more info
##########################

# TODO:

# - use data->after @ end of comments to do full threads
# - count comments and see if we have them all before crawling more
# - more efficient crawling?

# - http://docs.python-requests.org/en/latest/index.html and then:
# - setup reddit account and integrate api, respond to a comment!

# - implement regex flagging
# - implement responses

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

# Delete old links and comments
if len(argv) == 1 or 'cleanup' in argv:
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
        links.get("%s?limit=%d" % (l[1], _['links_per_page']))
        cur.execute("update crawl_locations set last_crawled = now() where id = %s", (l[0],))
        db.commit()

# Crawl eligible links
if len(argv) == 1 or 'comments' in argv:
    cur.execute("select id, permalink from t3 where last_crawled < date_sub(now(), interval %s second)", (_['recrawl_links_after'],))
    for c in cur.fetchall():
        for sort in _['comment_sort']:
            comments.get("http://www.reddit.com%s.json?limit=%d&depth=%d&sort=%s" % (c[1], _['comment_limit'], _['comment_depth'], sort))
            cur.execute("update t3 set last_crawled = now() where id = %s", (c[0],))
            db.commit()
            sleep(_['sleep'])

stats.printStats()

# Remove all data from database and logfile
if 'wipe' in argv:
    log.wipe()
    cur.execute("drop table if exists crawl_locations")
    cur.execute("drop table if exists t3")
    cur.execute("drop table if exists t1")
    db.commit()
    print "Data Wiped!!"

db.close()

if _['logging']: log.close()