import json
import re
import time
import pprint #delete me

from conf import _

from init import db, cur, opener
import lib
import log
import user

quotedRE = re.compile("^&gt;.*$", re.I|re.M)

for i in range(len(_['rules'])):
    if "regex" in _['rules'][i]:
        _['rules'][i]['re'] = re.compile(_["rules"][i]["regex"], re.I|re.M)

cur.execute("select distinct thing_id from responses")
responses = cur.fetchall()



def processComment(cid, body, author):
    for rule in _['rules']:
        if "flags" in rule and "ignoreQuotedText" in rule["flags"]:
            body = re.sub(quotedRE, "", body)

        if "flags" not in rule or ("flags" in rule and "selftextOnly" not in rule['flags']):
            if "user_function" in rule:
                print "*** process comment with userfunction"
            elif "regex" in rule and "response" in rule and "re" in rule:
                match = rule['re'].search(body)
                if match:
                    respond("t1_%s" % lib.base36encode(cid), rule, match, author)
                    break
            elif "string" in rule and "response" in rule:
                if rule["string"] in body:
                    respond("t1_%s" % lib.base36encode(cid), rule, None, author)
                    break




def processSelftext(lid, body, author):
    for rule in _['rules']:
        if "flags" in rule and "ignoreQuotedText" in rule["flags"]:
            body = re.sub(quotedRE, "", body)

        if "flags" not in rule or ("flags" in rule and "commentsOnly" not in rule['flags']):
            if "user_function" in rule:
                print "*** process selftext with userfunction"
            elif "regex" in rule and "response" in rule and "re" in rule:
                match = rule['re'].search(body)
                if match:
                    respond("t3_%s" % lib.base36encode(lid), rule, match, author)
                    break
            elif "string" in rule and "response" in rule:
                if rule["string"] in body:
                    respond("t3_%s" % lib.base36encode(lid), rule, None, author)
                    break



def respond(thing_id, rule, match, author):
    if "response" in rule:
        response = rule["response"]

        if "regex" in rule:
            which = 1
            for substr in match.groups():
                response = response.replace("$%d" % which, substr)
                which += 1

        response = response.replace("$author", author)
        postComment(thing_id, response)



def postComment(thing_id, text):
    global responses
    for response in responses:
        if thing_id in response[0]:
            return

    try: 
        success = False
        for i in range(_['http_retries']):
            f = opener.open('http://www.reddit.com/api/comment', 'api_type=json&thing_id=%s&text=%s' % (thing_id, text))
            if f.getcode() == 200:
                success = True
                break
            else:
                log.write('Error %d for reply attempt to %s' % (f.getcode(), thing_id), 'error')
                if f.getcode() in [401, 403, 404]: 
                    return
                time.sleep(_['sleep'])

        if success == False:
            log.write('Retries exhausted for reply to %s' % thing_id, 'error');
            return

        time.sleep(_['sleep'])

    except Exception, e:
        log.write('Error replying to %s: %s' % (thing_id, e), 'error')
        return

    rJSON = f.read()
    f.close()

    try: res = json.loads(rJSON)
    except Exception, e:
        log.write('Error parsing comment reply to %s response: %s' % (thing_id, e), 'error')
        return

    if "json" in res and "errors" in res["json"] and ("RATELIMIT" in res["json"]["errors"] or "SUBREDDIT_RATELIMIT" in res["json"]["errors"]):
        log.write('Ratelimited while replying to %s' % thing_id, 'error')
    else:
        try:
            cur.execute("insert into responses (thing_id, response) values (%s, %s)", (thing_id, text))
            db.commit()
        except Exception, e:
            log.write('Error storing response: %s' % e, 'error')
            return


