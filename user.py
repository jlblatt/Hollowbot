import json
import time

from conf import _

from init import opener, db, cur
import log

isLoggedIn = False

def checkLogin():
    global isLoggedIn

    cur.execute("select cookie, modhash from session")
    if cur.rowcount is 0:
        return
    else:
        for s in cur.fetchall():
            opener.addheaders.append(('Cookie', 'reddit_session=%s' % s[0]))
            opener.addheaders.append(('X-Modhash', s[1]))

    try:
        success = False
        for i in range(_['http_retries']):
            f = opener.open('http://www.reddit.com/api/me.json')
            if f.getcode() == 200:
                success = True
                break
            else:
                log.write('Error %d for login status check attempt' % f.getcode(), 'error')
                if f.getcode() in [401, 403, 404]: 
                    return
                time.sleep(_['sleep'])

        if success == False:
            log.write('Retries exhausted for login status check', 'error');
            return

        time.sleep(_['sleep'])
    except Exception, e:
        log.write('Error checking login status: %e' %e, 'error')
        return

    rJSON = f.read()
    f.close()

    try: res = json.loads(rJSON)
    except Exception, e:
        log.write('Error parsing login status response: %s' % e, 'error')
        return

    if 'data' in res:
        opener.addheaders.append(('X-Modhash', res['data']['modhash']))
        try:
            cur.execute("update session set modhash = %s", (res['data']['modhash'],))
            db.commit()
        except Exception, e:
            log.write('Error updating modhash: %s' % e, 'error')
            return
        isLoggedIn = True


def login():
    log.write('Logging in user %s' % _['reddit_username'], 'message')

    try: 
        success = False
        for i in range(_['http_retries']):
            f = opener.open('http://www.reddit.com/api/login', 'api_type=json&user=%s&passwd=%s' % (_['reddit_username'], _['reddit_password']))
            if f.getcode() == 200:
                success = True
                break
            else:
                log.write('Error %d for login attempt' % f.getcode(), 'error')
                if f.getcode() in [401, 403, 404]: 
                    return
                time.sleep(_['sleep'])

        if success == False:
            log.write('Retries exhausted for login', 'error');
            return

        time.sleep(_['sleep'])

    except Exception, e:
        log.write('Error logging in: %e' %e, 'error')
        return

    rJSON = f.read()
    f.close()

    try: res = json.loads(rJSON)
    except Exception, e:
        log.write('Error parsing login response: %s' % e, 'error')
        return

    opener.addheaders.append(('Cookie', 'reddit_session=%s' % res['json']['data']['cookie']))
    opener.addheaders.append(('X-Modhash', res['json']['data']['modhash']))

    try:
        cur.execute("delete from session")
        cur.execute("insert into session (modhash, cookie) values (%s, %s)", (res['json']['data']['modhash'],res['json']['data']['cookie']))
        db.commit()
    except Exception, e:
        log.write('Error storing login cookie/modhash: %s' % e, 'error')
        return

    isLoggedIn = True