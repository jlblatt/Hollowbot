import re
import pprint #delete me

from conf import _

from init import db, cur, opener
import lib
import user

for i in range(len(_['rules'])):
    if "regex" in _['rules'][i]:
        _['rules'][i]['re'] = re.compile(_["rules"][i]["regex"])



def processComment(cid, body, author):
    #print "Processing comment t1_%s" % lib.base36encode(cid)
    for rule in _['rules']:
        if "flags" not in rule or ("flags" in rule and "selftextOnly" not in rule['flags']):
            if "user_function" in rule:
                print "*** process comment with userfunction"
            elif "regex" in rule and "response" in rule and "re" in rule:
                if rule['re'].search(body):
                    print 'comment flagged!'
                    break
            elif "string" in rule and "response" in rule:
                if rule["string"] in body:
                    print 'comment flagged!'
                    break




def processSelftext(lid, body, author):
    #print "Processing selftext for link t3_%s" % lib.base36encode(lid)
    for rule in _['rules']:
        if "flags" not in rule or ("flags" in rule and "commentsOnly" not in rule['flags']):
            if "user_function" in rule:
                print "*** process selftext with userfunction"
            elif "regex" in rule and "response" in rule and "re" in rule:
                if rule['re'].search(body):
                    print 'selftext flagged!'
                    break
            elif "string" in rule and "response" in rule:
                if rule["string"] in body:
                    print "selftext flagged!"
                    break