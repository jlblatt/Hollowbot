import json
import time

from conf import _

from init import opener
import log

isLoggedIn = False
cookie = None
modhash = None

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

    global cookie
    global modhash
    cookie = res['json']['data']['cookie']
    modhash = res['json']['data']['modhash']

    isLoggedIn = True