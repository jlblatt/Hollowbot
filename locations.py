from conf import _

from init import db, cur, opener
import log

def build(crawl_subreddits, crawl_urls):
    urls = []

    log.write("Building location list...", 'message')

    for subreddit in crawl_subreddits:
        for sort in subreddit['sort']:
            if sort == "all": sort = ""
            urls.append("http://www.reddit.com/r/" + subreddit['subreddit'] + "/" + sort + ".json")

    for url in crawl_urls:
        urls.append(url + ".json")

    for url in urls:
        try:
            cur.execute("select id from crawl_locations where url = %s", (url,))
            if cur.rowcount > 0:
                cur.execute("update crawl_locations set last_seen = now() where url = %s", (url,))
            else:
                cur.execute("""insert into crawl_locations (
                                url,
                                last_seen,
                                last_crawled
                            ) values (%s, now(), 0)""", (
                                url
                            ))
            db.commit()

        except Exception, e:
            log.write('Error storing location: ' + url + ': %s' % e, 'exception')
            db.rollback()