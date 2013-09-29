ccount = 0

def getComments(url):
    global ccount

    printlog("Getting comments from: " + url + "...", 'message')
    start = time.time()
    
    try:
        f = opener.open(url)
    except Exception, e:
        printlog('Error opening links datasource: %s'  % e, 'error')
        return

    rJSON = f.read()
    f.close()

    try: comments = json.loads(rJSON)
    except Exception, e:
        printlog('Error parsing comments file: %s' % e, 'error')
        return

    ccount = 0
    getComment(comments)
    COMMENT_TIMES['counts'].append(ccount)
    COMMENT_TIMES['times'].append(time.time() - start)



def getComment(nodes):
    global ccount

    for node in nodes:
        try:
            if node['kind'] == 't1':
                try:
                    cur.execute("""replace into t1 (
                                    id,
                                    link_id,
                                    parent_id,
                                    body, 
                                    author,
                                    created,
                                    last_seen
                                ) values (%s, %s, %s, %s, %s, %s, now())""", (
                                    base36decode(node['data']['id']), 
                                    node['data']['link_id'],
                                    node['data']['parent_id'], 
                                    node['data']['body'], 
                                    node['data']['author'], 
                                    datetime.datetime.fromtimestamp(node['data']['created_utc'])
                                ))
                    db.commit()
                    ccount += 1

                    if node['data']['replies'] != "":
                        getComment([node['data']['replies']])

                except Exception, e:
                    printlog('Error storing t1_' + node['data']['id'] + ': %s' % e, 'exception')
                    db.rollback()

            elif node['kind'] == "Listing":
                getComment(node['data']['children']) 

        except Exception, e:
            printlog('Error checking comments file node type: %s' % e, 'exception')