###################################################################
# Hollowbot v1
# > Jason Blatt
############################################
# >> Email: jlblatt+hollowbot@gmail.com
# >> Git: https://github.com/jlblatt/Hollowbot
# >> See README and conf.py for more info
##########################

# TODO:

# - implement regex flagging
# - implement responses (comment and selftext)
# - respond to a comment and selftext!
# - store responses so we don't doublepost

from sys import argv
from time import sleep

from conf import _

from init import db, cur
import log
import lib
import locations
import links
import comments
import stats
import user

# Delete old links and comments
if 'runall' in argv or 'cleanup' in argv:
    if _['delete_links_after'] > -1: cur.execute("delete from t3 where created < date_sub(now(), interval %s second)", (_['delete_links_after'],))
    if _['delete_comments_after'] > -1: cur.execute("delete from t1 where created < date_sub(now(), interval %s second)", (_['delete_comments_after'],))
    db.commit();

# Build/store locations to retrieve links
if 'runall' in argv or 'locations' in argv:
    locations.build(_['crawl_subreddits'], _['crawl_urls'])

# Crawls URLS from locations
if 'runall' in argv or 'links' in argv:
    cur.execute("select id, url from crawl_locations where last_crawled < date_sub(now(), interval %s second)", (_['find_links_after'],))
    for l in cur.fetchall():
        links.get("%s?limit=%d" % (l[1], _['links_per_page']))
        cur.execute("update crawl_locations set last_crawled = now() where id = %s", (l[0],))
        db.commit()

# Crawl eligible links
if 'runall' in argv or 'comments' in argv:
    cur.execute("select id, permalink from t3 where last_crawled < date_sub(now(), interval %s second)", (_['recrawl_links_after'],))
    for c in cur.fetchall():
        for sort in _['comment_sort']:
            comments.get("http://www.reddit.com%s" % c[1], 't3_' + lib.base36encode(c[0]).lower(), '', "limit=%d&depth=%d&sort=%s" % (_['comment_limit_per_request'], _['comment_depth_per_request'], sort))
            cur.execute("update t3 set last_crawled = now() where id = %s", (c[0],))
            db.commit()
            sleep(_['sleep'])

#Login and respond to links/comments
if 'runall' in argv or 'respond' in argv:
    user.checkLogin()
    if not user.isLoggedIn: user.login()
    if user.isLoggedIn:
        print "Here"
    else:
        log.write("Error: could not log in, responses skipped", "error")

stats.printStats()

if len(argv) == 1:
    print "No arguments found, try 'python hollowbot.py runall' or check the README"

# Remove all data from database and logfile
if 'wipe' in argv:
    log.wipe()
    cur.execute("drop table if exists session")
    cur.execute("drop table if exists crawl_locations")
    cur.execute("drop table if exists t3")
    cur.execute("drop table if exists t1")
    db.commit()
    print "Data Wiped!!"

db.close()

if _['logging']: log.close()