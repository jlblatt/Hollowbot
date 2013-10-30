import datetime
import json
import time
import urllib2

from conf import _

from init import db, cur, opener
import log
import lib
import stats

lcount = 0

def get(url):
    log.write("Getting %d pages of %d links from: %s..." % (_['page_limit'], _['links_per_page'], url), 'message')
    start = time.time()

    after = ''

    for p in range(_['page_limit']):

        if after is None: break

        if after != '': finalUrl = url + '&after=' + after
        else: finalUrl = url

        try: f = opener.open(finalUrl)
        except Exception, e:
            log.write('Error opening links datasource: %s'  % e, 'error')
            return

        rJSON = f.read()
        f.close()

        try: links = json.loads(rJSON)
        except Exception, e:
            log.write('Error parsing links file: %s' % e, 'error')
            return

        after = links['data']['after']

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

        #endfor l in links

        stats.linkTimes['counts'].append(len(links['data']['children']))
        stats.linkTimes['times'].append(time.time() - start)

        time.sleep(_['sleep'])

    #endfor p in pages
