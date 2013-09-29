def getLinks(url):
    printlog("Getting links from: " + url + "...", 'message')
    start = time.time()

    try:
        if url.find('http') == 0: f = opener.open(url)
        else: f = open(url, "r")
    except Exception, e:
        printlog('Error opening links datasource: %s'  % e, 'exception')
        return

    rJSON = f.read()
    f.close()

    try: links = json.loads(rJSON)
    except Exception, e:
        printlog('Error parsing links file: %s' % e, 'exception')
        return

    for l in links['data']['children']:
        try:
            try:
                if l['kind'] == 't3':
                    cur.execute("""replace into t3 (
                                    id, 
                                    title, 
                                    url, 
                                    permalink, 
                                    created_utc,
                                    last_seen,
                                    last_crawled
                                ) values (%s, %s, %s, %s, %s, now(), 0)""", (
                                    base36decode(l['data']['id']), 
                                    l['data']['title'], 
                                    l['data']['url'], 
                                    l['data']['permalink'], 
                                    datetime.datetime.fromtimestamp(l['data']['created_utc'])
                                ))
                    db.commit()

            except Exception, e:
                printlog('Error storing t3_' + l['data']['id'] + ': %s' % e, 'exception')
                db.rollback()

        except Exception, e:
            printlog('Error checking links file node type: %s' % e, 'exception')

    LINK_TIMES['counts'].append(len(links['data']['children']))
    LINK_TIMES['times'].append(time.time() - start)
    return links['data']['after']
