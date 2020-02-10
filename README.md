# instagram scraper

instagramScraper is an application written in Python that crawls and scrapes an instagram user's posts and comments. 

It fetches a list of desired number of links to posts by any user, the caption for each post, the number of likes and the timestamp of when the post was done.
From the posts it saves the comments, username of the commenting person and the timestamp as well.

In order to get access to more posts, it also can log you in into your account.
If you use the authentication, the program will cache the user session by default so one doesn't need to create a new session every time.

With the database functionality you can save everything in a database. Here PostgreSQL.

Please use responsibly.


## Getting Started

Download the project via git clone and run the following:

```
pip install -r requirements.txt
```


### Prerequisites

selenium webdriver for Firefox: it requires the geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

You can download the executable here: https://github.com/mozilla/geckodriver/releases

psycopg2 for a PostgreSQL driver


### Limit recommendatios

Depending on your internet connection it is recommended to use time.sleep() so the drives has enough time to load the contents of the site.
The explicit brakes in this code are appropriate for an internet connection of 98 Mbps.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


