#!/usr/bin/python

###################################################################
# Hollowbot 1.0b
# > Jason Blatt
############################################
# >> Email: jlblatt+hollowbot@gmail.com
# >> Git: https://github.com/jlblatt/Hollowbot
# >> See README and conf.py for more info
##########################

# TODO:

# - improve regex matching (test regex special edgecases and try different string formatting)
# - put key check when accessing conf array _[]
# - redo crawl/rules
# - refine example-conf
# - BUILD A WEB INTERFACE MF

from sys import argv
from time import sleep

from conf import _

from init import db, cur
import comments
import lib
import links
import locations
import log
import respond
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
    for l in cur.fetchall():
        for sort in _['comment_sort']:
            comments.get("http://www.reddit.com%s" % l[1], 't3_' + lib.base36encode(l[0]).lower(), '', "limit=%d&depth=%d&sort=%s" % (_['comment_limit_per_request'], _['comment_depth_per_request'], sort))
            cur.execute("update t3 set last_crawled = now() where id = %s", (l[0],))
            db.commit()
            sleep(_['sleep'])

#Login and respond to links/comments
if 'runall' in argv or 'respond' in argv:
    log.write("Checking for existing session...", "message")
    user.checkLogin()
    if not user.isLoggedIn: user.login()
    
    if user.isLoggedIn:
        log.write("Processing text and responding...", "message")
        
        #Process selftext
        cur.execute("select id, content, author from t3 where content is not null")
        for c in cur.fetchall():
            respond.processSelftext(c[0], c[1], c[2])
        
        #Process comments
        cur.execute("select id, body, author from t1")
        for c in cur.fetchall():
            respond.processComment(c[0], c[1], c[2])

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
    cur.execute("drop table if exists responses")
    db.commit()
    print "Data Wiped!!"

db.close()

if _['logging']: log.close()