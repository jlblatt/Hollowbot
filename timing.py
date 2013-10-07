import time
from logging import printLog

START_TIME = time.time()
LINK_TIMES = {'counts' : [] , 'times' : []}
COMMENT_TIMES = {'counts' : [] , 'times' : []}

def printStats():
    printLog(str(sum(LINK_TIMES['counts'])) + " links / " + str(sum(LINK_TIMES['times'])) + " sec. (" + str(sum(LINK_TIMES['times']) / sum(LINK_TIMES['counts'])) + " sec. ea.) in " + str(len(LINK_TIMES['counts'])) + " locations", 'stat')
    printLog(str(sum(COMMENT_TIMES['counts'])) + " comments / " + str(sum(COMMENT_TIMES['times'])) + " sec. (" + str(sum(COMMENT_TIMES['times']) / sum(COMMENT_TIMES['counts'])) + " sec. ea.) in " + str(len(COMMENT_TIMES['counts'])) + " locations", 'stat')
    printLog("Execution took " + str(time.time() - START_TIME) + " sec.", 'stat')

