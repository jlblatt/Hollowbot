try: db = MySQLdb.connect(host=_['db_host'], db=_['db_name'], user=_['db_user'], passwd=_['db_pass'], charset='utf8')
except Exception, e:
    printlog("Can't open database connection: " + ': %s' % e, 'exception')
    exit(1)

cur = db.cursor()

try: cur.execute("""create table if not exists t3 (
                        id bigint(1) not null, 
                        title text, 
                        url text, 
                        permalink text,
                        created_utc timestamp,
                        last_seen timestamp,
                        last_crawled timestamp,
                        primary key(id)
                    ) engine=InnoDB character set=utf8""")
except Exception, e:
    printlog("Can't create table `t3`: " + ': %s' % e, 'exception')
    exit(1)

try: cur.execute("""create table if not exists t1 (
                        id bigint(1) not null,
                        link_id text,
                        parent_id text,
                        body text, 
                        author text,
                        created_utc timestamp,
                        last_seen timestamp,
                        primary key(id)
                    ) engine=InnoDB character set=utf8""")
except Exception, e:
    printlog("Can't create table `t1`: " + ': %s' % e, 'exception')
    exit(1)

try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', _['name'] + ' ' + _['version'] + ' (' + _['description'] + ') by ' + _['author'] + ' | ' + _['author_url'] + ' | ' + _['author_email'])]
except Exception, e:
    printlog("Can't create urllib2 opener: " + ': %s' % e, 'exception')
    exit(1)