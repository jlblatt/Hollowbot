import datetime

from conf import _

if _['logging']:
    try: log = open(_['logfile'], "a")
    except Exception, e:
        print "Can't open log file: " + ': %s' % e

def write(msg, msg_type):
    print msg
    if _['logging'] and msg_type in _['logtypes']:
        try: log.write("[" + str(datetime.datetime.now()) + "] " + msg + "\n")
        except Exception, e:
            print "Can't write log file: " + ': %s' % e