**Read this entire file before doing anything.  It's really not that long and will keep you from getting yourself banned.**

# Description

Hollowbot is an attempt to create an open-source framework for a reddit bot to crawl, interpret, and respond to comments.  Users deploying the bot can provide a configuration/ruleset to control its behavior.

/r/hollowbot is its testing sub.

Hollowbot is currently in ALPHA.

# Quickstart
 
1. Move `example-conf.json` to `conf.json` and replace default values with your own (bot info, database credentials, etc...)
2. Remove the `quit` definition (2nd from bottom) from `conf.json`
3. Run `python hollowbot.py`

# Command Line Arguments

Hollowbot accepts several command line arguments to control which functions to perform.  They are listed below in order of execution.  Running the bot without any arguments performs all functions except 'wipe'.

* `wipe` - delete all stored data and log files when complete
* `cleanup` - Remove old links/comments from database
* `locations` - Build and store list of all locations to retrieve links
* `links` - Crawl URLs and retrieve links to comment threads
* `comments` - Get comments from all stored threads

# conf.json Fields

### Bot General Info

This information is concatinated and included in the User-Agent string

* `name`
* `version`
* `description`
* `author`
* `author_url`
* `author_email`

### Database Credentials

* `db_host`
* `db_name`
* `db_user`
* `db_pass`

### reddit Credentials

* `reddit_username`
* `reddit_password`

### Logging

* `logging` - When true, bot will attempt to write onscreen messages to a log file (specified below)
* `logtypes` - Array of message types to write to log.  Choices are: "exception", "error", "stat", "message"
* `logfile` - Path to log file

### Crawl Configuration
* `crawl_subreddits` - Array of objects bot should gather links from, with two fields each:
        * subreddit - name of the subreddit (what comes after r/...)
        * sort - array of sort techniques to retrieve results.  'all' is the default front page listing.  Other options are 'hot', 'new', 'rising', 'controversial', 'top', 'gilded'.
* `crawl_urls` - Array of additional URLs bot should gather links from (does not include .json or URL arguments)
* `page_limit` - Number of pages of links to fetch
* `links_per_page` - Number of links to fetch per page request (reddit's limit seems to be 100)
* `comment_limit_per_request` - Number of comments to fetch per comment thread request (reddit's limit seems to be 500)
* `comment_depth_per_request` - Depth of comment tree to retrieve per comment thread request (reddit's limit seems to be 8)
* `comment_depth_total` - Number of times to request a child comment thread if still incomplete.  0 = do not traverse child threads
* `comment_subling_total` - Number of times to request a sibling comment thread if still incomplete. 0 = do not traverse sibling threads 
* `comment_traverse_threshold` - Thread must have at least this many more comments to traverse children or siblings
* `autoget_lte_20` - Use /morechildren POST API to fetch remaining comments if count <= 20 (using depth of 8)
* `autoget_threshold` - Thread must have at least this many more comments to autoget
* `comment_sort` - array of sort techniques to retrieve results.  'confidence' is the default listing (aka 'best').  Other options are 'top', 'new', 'hot', 'controversial', 'old', 'random'.
* `find_links_after` - Time (in seconds) before recrawling a subreddit page or crawl url. 0 = always recrawl all pages
* `recrawl_links_after` - Time (in seconds) to recrawl comments from one thread (measured from the link's last crawled timestamp).  0 = always crawl all links
* `delete_links_after` - Time (in seconds) until a found link is removed from the database (measured from it's creation timestamp, **not** it's last crawled/seen timestamp).  0 = always delete links immediately.  -1 = never delete links.
* `delete_comments_after` - Time (in seconds) until a comment is removed from the database (measured from it's creation timestamp, **not** it's last crawled/seen timestamp).  0 = always delete comments immediately.  -1 = never delete comments.
* `http_retries` - Number of times to retry a page or comment url (known 401/403/404s are skipped immediately)
* `sleep` - Time (in seconds) to sleep between server requests (2 is recommended, see below)

## Reddit API Notice

https://github.com/reddit/reddit/wiki/API

We're happy to have API clients, crawlers, scrapers, and Greasemonkey scripts, but they have to obey some rules:

* Make no more than thirty requests per minute. This allows some burstiness to your requests, but keep it sane. On average, we should see no more than one request every two seconds from you.
* Change your client's User-Agent string to something unique and descriptive, preferably referencing your reddit username.
    * Example: User-Agent: flairbot/1.0 by spladug
    * Many default User-Agents (like "Python/urllib" or "Java") are drastically limited to encourage unique and descriptive user-agent strings.
    * If you're making an application for others to use, please include a version number in the user agent. This allows us to block buggy versions without blocking all versions of your app.
    * NEVER lie about your user-agent. This includes spoofing popular browsers and spoofing other bots. We will ban liars with extreme prejudice.
* Most pages are cached for 30 seconds, so you won't get fresh data if you request the same page that often. Don't hit the same page more than once per 30 seconds.
* Requests for multiple resources at a time are always better than requests for single-resources in a loop. Talk to us on the mailing list or in #reddit-dev if we don't have a batch API for what you're trying to do.
* Our robots.txt is for search engines not API clients. Obey these rules for API clients instead.

https://github.com/reddit/reddit/wiki/API