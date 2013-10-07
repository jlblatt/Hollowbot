# Description

Hollowbot is an attempt to create an open-source framework for a reddit bot to crawl, interpret, and respond to comments.  Users deploying the bot can provide a configuration/ruleset to control its behavior.

/r/hollowbot is its testing sub.

Hollowbot is currently in ALPHA.

# Quickstart

1. Read this entire file before doing anything
2. Move example-conf.json to conf.json and replace default values with your own (bot info, database credentials, etc...)
3. Remove the 'quit' definition (2nd from bottom) from conf.json
4. Run hollowbot.py (don't forget to chmod +x)

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