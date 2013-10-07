import time
import log

startTime = time.time()
linkTimes = {'counts' : [] , 'times' : []}
commentTimes = {'counts' : [] , 'times' : []}

def printStats():
    log.write(str(sum(linkTimes['counts'])) + " links / " + str(sum(linkTimes['times'])) + " sec. (" + str(sum(linkTimes['times']) / sum(linkTimes['counts'])) + " sec. ea.) in " + str(len(linkTimes['counts'])) + " locations", 'stat')
    log.write(str(sum(commentTimes['counts'])) + " comments / " + str(sum(commentTimes['times'])) + " sec. (" + str(sum(commentTimes['times']) / sum(commentTimes['counts'])) + " sec. ea.) in " + str(len(commentTimes['counts'])) + " locations", 'stat')
    log.write("Execution took " + str(time.time() - startTime) + " sec.", 'stat')

