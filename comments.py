import datetime
import json
import time
import urllib2

import log
from init import db, cur, opener
from lib import *
from timing import commentTimes

ccount = 0

def get(url):
    global ccount

    log.write("Getting comments from: " + url + "...", 'message')
    start = time.time()
    
    try:
        f = opener.open(url)
    except Exception, e:
        log.write('Error opening links datasource: %s'  % e, 'error')
        return

    rJSON = f.read()
    f.close()

    try: comments = json.loads(rJSON)
    except Exception, e:
        log.write('Error parsing comments file: %s' % e, 'error')
        return

    ccount = 0
    getCommentTree(comments)
    commentTimes['counts'].append(ccount)
    commentTimes['times'].append(time.time() - start)



def getCommentTree(nodes):
    global ccount

    for node in nodes:
        try:
            if node['kind'] == 't1':
                try:
                    cur.execute("""replace into t1 (
                                    id,
                                    link_id,
                                    parent_id,
                                    body, 
                                    author,
                                    created,
                                    last_seen
                                ) values (%s, %s, %s, %s, %s, %s, now())""", (
                                    base36decode(node['data']['id']), 
                                    node['data']['link_id'],
                                    node['data']['parent_id'], 
                                    node['data']['body'], 
                                    node['data']['author'], 
                                    datetime.datetime.fromtimestamp(node['data']['created_utc'])
                                ))
                    db.commit()
                    ccount += 1

                    if node['data']['replies'] != "":
                        getCommentTree([node['data']['replies']])

                except Exception, e:
                    log.write('Error storing t1_' + node['data']['id'] + ': %s' % e, 'exception')
                    db.rollback()

            elif node['kind'] == "Listing":
                getCommentTree(node['data']['children']) 

        except Exception, e:
            log.write('Error checking comments file node type: %s' % e, 'exception')