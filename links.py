import datetime
import json
import time

from conf import _

from init import db, cur, opener
import log
import lib
import stats

lcount = 0

def get(url):
    log.write("Getting %d page(s) of %d links from: %s..." % (_['page_limit'], _['links_per_page'], url), 'message')
    start = time.time()

    after = ''

    for p in range(_['page_limit']):

        if after is None: break

        if after != '': finalUrl = url + '&after=' + after
        else: finalUrl = url

        try: 
            success = False
            for i in range(_['http_retries']):
                f = opener.open(finalUrl)
                if f.getcode() == 200:
                    success = True
                    break
                else:
                    log.write('Error %d for links url: %s' % (f.getcode(), finalUrl), 'error')
                    if f.getcode() in [401, 403, 404]: 
                        return
                    time.sleep(_['sleep'])

            if success == False:
                log.write('Retries exhausted for links url: %s' % finalUrl, 'error');
                return

            time.sleep(_['sleep'])

        except Exception, e:
            log.write('Error opening links url: %s - %s' % (finalUrl, e), 'error')
            return

        rJSON = f.read()
        f.close()

        try: links = json.loads(rJSON)
        except Exception, e:
            log.write('Error parsing links url: %s - %s' % (finalUrl, e), 'error')
            return

        after = links['data']['after']

        for l in links['data']['children']:
            try:
                if l['kind'] == 't3':
                    try:
                        cur.execute("select id from t3 where id = %s", (lib.base36decode(l['data']['id']),))
                        if cur.rowcount > 0:
                            cur.execute("update t3 set last_seen = now() where id = %s", (lib.base36decode(l['data']['id']),))
                        else:
                            if l['data']['is_self']: content = l['data']['selftext']
                            else: content = None;
                            
                            cur.execute("""insert into t3 (
                                            id, 
                                            title, 
                                            url, 
                                            permalink, 
                                            content,
                                            created,
                                            last_seen,
                                            last_crawled
                                        ) values (%s, %s, %s, %s, %s, %s, now(), 0)""", (
                                            lib.base36decode(l['data']['id']), 
                                            l['data']['title'], 
                                            l['data']['url'], 
                                            l['data']['permalink'],
                                            content,
                                            datetime.datetime.fromtimestamp(l['data']['created_utc'])
                                        ))
                        db.commit()

                    except Exception, e:
                        log.write('Error storing t3_' + l['data']['id'] + ': %s' % e, 'error')
                        db.rollback()

            except Exception, e:
                log.write('Error checking links file node type: %s' % e, 'error')

        #endfor l in links

        stats.linkTimes['counts'].append(len(links['data']['children']))
        stats.linkTimes['times'].append(time.time() - start)

        time.sleep(_['sleep'])

    #endfor p in pages
