import time

from init import cur, opener
import log

startTime = time.time()
linkTimes = {'counts' : [] , 'times' : []}
commentTimes = {'counts' : [] , 'times' : []}
responseTimes = {'counts' : [] , 'times' : []}


def printStats():
    cur.execute("select count(*) from crawl_locations")
    locationTotal = cur.fetchone()[0]

    linkLocations = len(linkTimes['counts'])
    linkCount = sum(linkTimes['counts'])
    linkElapsedTime = sum(linkTimes['times'])
    if linkCount == 0: linkRate = 0
    else: linkRate = linkElapsedTime / linkCount
    cur.execute("select count(*) from t3")
    linkTotal = cur.fetchone()[0]

    commentLocations = len(commentTimes['counts'])
    commentCount = sum(commentTimes['counts'])
    commentElapsedTime = sum(commentTimes['times'])
    if commentCount == 0: commentRate = 0
    else: commentRate = commentElapsedTime / commentCount
    cur.execute("select count(*) from t1")
    commentTotal = cur.fetchone()[0]

    responseLocations = len(responseTimes['counts'])
    responseCount = sum(responseTimes['counts'])
    responseElapsedTime = sum(responseTimes['times'])
    if responseCount == 0: responseRate = 0
    else: responseRate = responseElapsedTime / responseCount
    cur.execute("select count(*) from responses")
    responseTotal = cur.fetchone()[0]

    totalElapsed = time.time() - startTime

    log.write("%d link(s) / %f sec. (%f sec. ea.) in %d location(s)" % (linkCount, linkElapsedTime, linkRate, linkLocations), 'stat')
    log.write("%d comment(s) / %f sec. (%f sec. ea.) in %d thread(s)" % (commentCount, commentElapsedTime, commentRate, commentLocations), 'stat')
    log.write("%d response(s) / %f sec. (%f sec. ea.) in %d thread(s)" % (responseCount, responseElapsedTime, responseRate, responseLocations), 'stat')
    log.write("%d location(s) / %d link(s) / %d comment(s) / %d responses currently in database" % (locationTotal, linkTotal, commentTotal, responseTotal), 'stat')
    log.write("Execution took %f sec. (%f minutes)" % (totalElapsed, totalElapsed / 60), 'stat')

