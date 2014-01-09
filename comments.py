import datetime
import json
import time

from conf import _

from init import db, cur, opener
import log
import lib
import stats

ccount = 0

def get(url, linkid, commentid = '', args = '', depth = 0, post = False):

    if depth > _['comment_depth_total']: 
        return

    global ccount

    url = url.encode('ascii', 'ignore')

    if post:
        log.write("Autogetting <= 20 comments from: %s.json via POST: %s..." % (url + commentid, args), 'message')
    else:
        log.write("Getting %d comment(s) at depth %d from: %s.json?%s..." % (_['comment_limit_per_request'], depth, url + commentid, args), 'message')
    
    start = time.time()

    try: 
        success = False
        for i in range(_['http_retries']):
            if post:
                f = opener.open(url + commentid + '.json', args)
            else: 
                f = opener.open(url + commentid + '.json?' + args)
            
            if f.getcode() == 200:
                success = True
                break
            else:
                log.write('Error %d for comments url: %s' % (f.getcode(), url), 'error')
                if f.getcode() in [401, 403, 404]: 
                    return
                time.sleep(_['sleep'])

        if success == False:
            log.write('Retries exhausted for comments url: %s' % url, 'error');
            return

        time.sleep(_['sleep'])

    except Exception, e:
        log.write('Error opening comments url: %s - %s' % (url, e), 'error')
        return

    rJSON = f.read()
    f.close()

    try: comments = json.loads(rJSON)
    except Exception, e:
        log.write('Error parsing comments file: %s' % e, 'error')
        return

    ccount = 0
    
    if post:
        getCommentTree(comments['json']['data']['things'], url, linkid, commentid, args, depth)
    else:
        getCommentTree(comments, url, linkid, commentid, args, depth)

    stats.commentTimes['counts'].append(ccount)
    stats.commentTimes['times'].append(time.time() - start)



def getCommentTree(nodes, url, linkid, commentid, args, depth):
    global ccount

    for node in nodes:
        try:
            if node is None:
                break

            elif node['kind'] == 't1':
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
                        getCommentTree([node['data']['replies']], url, linkid, commentid, args, depth)

                except Exception, e:
                    log.write('Error storing t1_' + node['data']['id'] + ': %s' % e, 'error')
                    db.rollback()

            elif node['kind'] == "Listing":
                getCommentTree(node['data']['children'], url, linkid, commentid, args, depth)

            elif node['kind'] == "more":
                if _['autoget_lte_20'] and node['data']['count'] <= 20 and node['data']['count'] >= _['autoget_threshold']:
                    children = ",".join(node['data']['children'])
                    time.sleep(_['sleep'])
                    get('http://www.reddit.com/api/morechildren/', linkid, "", "api_type=json&depth=8&link_id=%s&children=%s" % (linkid, children), 0, True)

                elif node['data']['count'] >= _['comment_traverse_threshold']:
                    if node['data']['parent_id'] == linkid or node['data']['parent_id'] == commentid:
                        #sibling traversal
                        breadth = 0
                        for child in node['data']['children']:
                            if breadth >= _['comment_siblings_total']:
                                break
                            time.sleep(_['sleep'])
                            get(url, linkid, child, args, depth)
                            breadth += 1
                    else:
                        #child traversal
                        time.sleep(_['sleep'])
                        get(url, linkid, node['data']['parent_id'][3:], args, depth + 1)

        except Exception, e:
            log.write('Error checking comments file node type: %s' % e, 'error')