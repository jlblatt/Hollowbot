import datetime

from conf import _

if _['logging']:
    try: log = open(_['logfile'], "a")
    except Exception, e:
        print "Can't open log file: " + ': %s' % e

def write(msg, msg_type):
    global log

    print msg
    if _['logging'] and msg_type in _['logtypes']:
        try: log.write("[" + str(datetime.datetime.now()) + "] " + msg + "\n")
        except Exception, e:
            print "Can't write log file: " + ': %s' % e

def wipe():
    global log
    
    if _['logging']: log.close()
    try: log = open(_['logfile'], "w")
    except Exception, e:
        print "Couldn't wipe log file: " + ': %s' % e