import datetime
import json
import time
import urllib2

from init import db, cur, opener
import log
import lib
import stats

def get(url):
    log.write("Getting links from: " + url + "...", 'message')
    start = time.time()

    try: f = opener.open(url)
    except Exception, e:
        log.write('Error opening links datasource: %s'  % e, 'error')
        return

    rJSON = f.read()
    f.close()

    try: links = json.loads(rJSON)
    except Exception, e:
        log.write('Error parsing links file: %s' % e, 'error')
        return

    for l in links['data']['children']:
        try:
            try:
                if l['kind'] == 't3':
                    cur.execute("select id from t3 where id = %s", (lib.base36decode(l['data']['id']),))
                    if cur.rowcount > 0:
                        cur.execute("update t3 set last_seen = now() where id = %s", (lib.base36decode(l['data']['id']),))
                    else:
                        cur.execute("""insert into t3 (
                                        id, 
                                        title, 
                                        url, 
                                        permalink, 
                                        created,
                                        last_seen,
                                        last_crawled
                                    ) values (%s, %s, %s, %s, %s, now(), 0)""", (
                                        lib.base36decode(l['data']['id']), 
                                        l['data']['title'], 
                                        l['data']['url'], 
                                        l['data']['permalink'], 
                                        datetime.datetime.fromtimestamp(l['data']['created_utc'])
                                    ))
                    db.commit()

            except Exception, e:
                log.write('Error storing t3_' + l['data']['id'] + ': %s' % e, 'exception')
                db.rollback()

        except Exception, e:
            log.write('Error checking links file node type: %s' % e, 'exception')

    stats.linkTimes['counts'].append(len(links['data']['children']))
    stats.linkTimes['times'].append(time.time() - start)
    return links['data']['after']
