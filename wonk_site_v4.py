from flask import Flask, render_template, session, redirect, url_for

from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask.ext.moment import Moment

import feedparser
import re
import sqlite3
import twitter

app = Flask("Top Wonks")
app.config['SECRET_KEY'] = 'hard to guess string 123'
moment = Moment(app)

bootstrap = Bootstrap(app)

dbconn = sqlite3.connect("wonk.db")
c = dbconn.cursor()
topic_list = list(c.execute("select w.wonk_id, w.name, t.topic from wonk_topics t, wonks w where w.wonk_id = t.wonk_id order by w.wonk_id"))

rss_feed_list = (
    'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
    'http://rss.nytimes.com/services/xml/rss/nyt/Economy.xml',
    'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    )

@app.route('/')
def index():

    html_string = " "

    for rss_url in rss_feed_list:
        d = feedparser.parse(rss_url)
        for e in d.entries:
            html_string += "<tr>"
            m = re.match("[^<>]+",e.summary_detail.value)
            v = m.group(0)
            html_string += '<td><a href="%s">%s</a><br>%s (%s)</td>' % (
                e.links[0].href, e.title, v, e.updated
                )
            html_string += "<td>"

            wonk_entered = -1
            for topic_entry in topic_list:
                if (topic_entry[0] != wonk_entered): # don't enter the same wonk again
                    if (re.search(topic_entry[2], e.title,re.IGNORECASE)):
                        wonk_entered = topic_entry[0]
                        html_string += make_wonk_link(topic_entry[1],wonk_entered)
                    elif (re.search(topic_entry[2], v,re.IGNORECASE)):
                        wonk_entered = topic_entry[0]
                        html_string += make_wonk_link(topic_entry[1],wonk_entered)

            html_string += "</td>"
            html_string += "</tr>"

    return render_template("news_stories.html",html_stuff=html_string)

@app.route('/wonk/<wonk_number>')
def wonk_page(wonk_number):
    wonk_name = wonk_number
    dbconn = sqlite3.connect("wonk.db")
    c = dbconn.cursor()
    arguments = (wonk_number,)
    for row in c.execute("select name,blog_url from wonks where wonk_id = ?",arguments):
        (wonk_name, blog_url) = row

    blog_list = ()
    if (blog_url):
        d = feedparser.parse(blog_url)
        if (d):
            blog_list = d.entries

    return render_template("wonk_info.html", wonk_name=wonk_name, blog_list=blog_list)

def make_wonk_link(name,number):
    wonk_url = '/wonk/%s' % number
    return ('<a href=%s>%s</a>&nbsp;' % (wonk_url,name))

class FindWonk(Form):
    name = StringField("Wonk name:",validators=[Required()])
    submit = SubmitField('Find the wonk.')

@app.route('/wonkadmin',methods=['GET','POST'])
def wonk_admin():
    form = FindWonk()
    if form.validate_on_submit():
        return redirect(url_for('wonk_admin'))
    return render_template('wonk_admin_form.html',form=form)



if __name__ == '__main__':
    app.run(debug=True)
