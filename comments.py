import datetime
import json
import time
import urllib2

from conf import _

from init import db, cur, opener
import log
import lib
import stats

ccount = 0

def get(url):
    global ccount

    url = url.encode('ascii', 'ignore')

    log.write("Getting %d comments at depth %d from: %s..." % (_['comment_limit'], _['comment_depth'], url), 'message')
    start = time.time()
    
    try: f = opener.open(url)
    except Exception, e:
        log.write('Error opening comments datasource: %s'  % e, 'error')
        return

    rJSON = f.read()
    f.close()

    try: comments = json.loads(rJSON)
    except Exception, e:
        log.write('Error parsing comments file: %s' % e, 'error')
        return

    ccount = 0
    getCommentTree(comments)
    stats.commentTimes['counts'].append(ccount)
    stats.commentTimes['times'].append(time.time() - start)



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
                                    lib.base36decode(node['data']['id']), 
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