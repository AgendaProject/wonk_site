
import feedparser
import re
import twitter

import MySQLdb

from dateutil.parser import parse

def get_blog_entries():
    dbconn = MySQLdb.connect("mysql.server","mpearl","readyforgranny","mpearl$wonk_db")
    c = dbconn.cursor()

    dbconn.set_character_set('utf8')
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    c.execute("select wonk_id, name, bio_url, blog_url from wonks where blog_url is not null order by wonk_id")
    wonk_list = c.fetchall()
    count = 0
    for row in wonk_list:
        (wonk_id, wonk_name, wonk_url, blog_url) = row
        if (blog_url):
            d = feedparser.parse(blog_url)
            if (d):
                for entry in d.entries:
                    try:
                        dd = parse(entry.updated,ignoretz=True,fuzzy=True)
                    except:
                        dd = parse("1/1/1960",ignoretz=True,fuzzy=True)
                    if (getattr(entry,"title",False)  and getattr(entry,"links",False) and getattr(entry,"summary_detail",False)):
                        c.execute("insert into wonk_news_entries (wonk_id, title, blog_href, summary, wonk_name, wonk_url, entry_date) values (%s, %s, %s, %s, %s, %s, %s)",
                                  (wonk_id, entry.title, entry.links[0].href, entry.summary_detail.value, wonk_name, wonk_url, dd))
                        dbconn.commit()
                        count = count + 1
                        print "Count ",count

get_blog_entries()
