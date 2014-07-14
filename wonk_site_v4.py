from time import strptime
from flask import Flask, render_template, session, redirect, url_for

from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextField,TextAreaField
from wtforms.validators import Required

from flask.ext.moment import Moment

import feedparser
import re
import sqlite3
import twitter

import MySQLdb

print "Hello from Democracy Top Wonks!!"

app = Flask("Top Wonks")
app.config['SECRET_KEY'] = '2264636714'
moment = Moment(app)

bootstrap = Bootstrap(app)

date_format = "%Y-%m-%dT%H:%M:%S"

@app.route('/')
def index():
    dbconn = MySQLdb.connect("mysql.server","mpearl","readyforgranny","mpearl$wonk_db")
    c = dbconn.cursor()
    c.execute("select wonk_id, name, web_url, blog_url from wonks order by wonk_id")
    wonk_list = c.fetchall()
    blog_entry_list = []
    for row in wonk_list:
        (wonk_id, wonk_name, wonk_url, blog_url) = row
        if (blog_url):
            d = feedparser.parse(blog_url)
            if (d):
                for entry in d.entries:
                    e = (strptime(entry.updated[:-7],date_format),wonk_id, wonk_name, wonk_url, entry)
                    # The last seven characters seem to be the timezone, but in the wrong format, so ignore.
                    blog_entry_list.append(e)
    blog_entry_list.sort(key=lambda x:x[0], reverse=True)
    # we want to stort on the first column, the timestamp, and have the latest entries first.
    return render_template("wonk_blog_entry_list.html", blog_list=blog_entry_list)

class EditWonk(Form):
    name = TextField("Wonk name:",validators=[Required()])
    blog_url = TextField("Blog URL:")
    bio = TextAreaField("Biography:")
    submit = SubmitField('Save Changes')

@app.route('/wonkedit/<wonk_number>',methods=['GET','POST'])
def edit_wonk(wonk_number):
    f = EditWonk()
    dbconn = MySQLdb.connect("mysql.server","mpearl","readyforgranny","mpearl$wonk_db")
    with dbconn:
        c = dbconn.cursor()

        if f.validate_on_submit():
            print "Name >>> ",f.name.data
            print "New BIO >>> ",f.bio.data
            print "New Blog URL >>> ",f.blog_url.data
            c.execute('update wonks set bio = %s where wonk_id = %s', (f.bio.data,wonk_number))
        
    arguments = (wonk_number)
    c.execute("select name,blog_url, bio from wonks where wonk_id = %s",arguments)
    row_list = c.fetchall()

    for row in row_list:
        (f.name.data, f.blog_url.data, f.bio.data) = row
        return render_template("edit_wonk.html",form=f)

@app.route('/wonk/<wonk_number>')
def wonk_page(wonk_number):
    wonk_name = wonk_number

    dbconn = MySQLdb.connect("mysql.server","mpearl","readyforgranny","mpearl$wonk_db")
    c = dbconn.cursor()

    arguments = (wonk_number)
    c.execute("select name,blog_url, bio from wonks where wonk_id = %s",arguments)
    row_list = c.fetchall()
    for row in row_list:
        (wonk_name, blog_url, wonk_bio_info) = row

    blog_list = ()
    if (blog_url):
        d = feedparser.parse(blog_url)
        if (d):
            blog_list = d.entries

    return render_template("wonk_info.html", wonk_name=wonk_name, wonk_bio_info=wonk_bio_info, blog_list=blog_list)

def make_wonk_link(name,number):
    wonk_url = '/wonk/%s' % number
    return ('<a href=%s>%s</a>&nbsp;' % (wonk_url,name))

class FindWonk(Form):
    name = StringField("Wonk name:",validators=[Required()])
    submit = SubmitField('Find the wonk.')

@app.route('/wonkadmin',methods=['GET','POST'])
def wonk_admin():
    form = FindWonk()
    h_string = " "
    if form.validate_on_submit():
        dbconn = MySQLdb.connect("mysql.server","mpearl","readyforgranny","mpearl$wonk_db")
        c = dbconn.cursor()
        arguments = (form.name.data)
        c.execute("select wonk_id,name from wonks where name REGEXP %s",arguments)
        row_list = c.fetchall()
        for row in row_list:
            h_string += '<a href=/wonkedit/%s>%s</a><br>' % row
        return render_template('wonk_admin_list.html',html_stuff=h_string)
    return render_template('wonk_admin_form.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
