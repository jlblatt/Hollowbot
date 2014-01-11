import MySQLdb
import urllib2
import warnings

from conf import _
import log

warnings.filterwarnings('ignore', category = MySQLdb.Warning)

try: db = MySQLdb.connect(host=_['db_host'], db=_['db_name'], user=_['db_user'], passwd=_['db_pass'], charset='utf8')
except Exception, e:
    log.write("Can't open database connection: %s" % e, 'error')
    exit(1)

cur = db.cursor()

try: cur.execute("""create table if not exists session (
                        id bigint(1) not null,
                        cookie text,
                        modhash text,
                        primary key(id)
                    ) engine=InnoDB character set=utf8""")
except Exception, e:
    log.write("Can't create table `session`: %s" % e, 'error')
    exit(1)

try: cur.execute("""create table if not exists crawl_locations (
                        id bigint(1) not null auto_increment,
                        url text,
                        last_seen datetime,
                        last_crawled datetime,
                        primary key(id)
                    ) engine=InnoDB character set=utf8""")
except Exception, e:
    log.write("Can't create table `crawl_locations`: %s" % e, 'error')
    exit(1)

try: cur.execute("""create table if not exists t3 (
                        id bigint(1) not null, 
                        title text, 
                        url text,
                        permalink text,
                        content text,
                        author text,
                        created datetime,
                        last_seen datetime,
                        last_crawled datetime,
                        primary key(id)
                    ) engine=InnoDB character set=utf8""")
except Exception, e:
    log.write("Can't create table `t3`: %s" % e, 'error')
    exit(1)

try: cur.execute("""create table if not exists t1 (
                        id bigint(1) not null,
                        link_id text,
                        parent_id text,
                        body text, 
                        author text,
                        created datetime,
                        last_seen datetime,
                        primary key(id)
                    ) engine=InnoDB character set=utf8""")
except Exception, e:
    log.write("Can't create table `t1`: %s" % e, 'error')
    exit(1)

try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', _['name'] + ' ' + _['version'] + ' (' + _['description'] + ') by ' + _['author'] + ' | ' + _['author_url'] + ' | ' + _['author_email'])]
except Exception, e:
    log.write("Can't create urllib2 opener: %s" % e, 'error')
    exit(1)