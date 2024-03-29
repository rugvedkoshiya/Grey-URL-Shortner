from flask import Flask, render_template, request, redirect
import sqlite3
import validators
import random
from nanoid import generate

from config import Config as SETTING

config = SETTING()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        params = {'valid_check':'none', 'orignal_url': '', 'shorten_url': ''}
        return render_template('index.html', data=params)
    elif request.method == 'POST':
        orignal_url = request.form['url']
        # check that url is valid or not
        valid_check = validators.url(orignal_url)
        if not valid_check:
            params = {'valid_check':'block', 'orignal_url': f'{orignal_url}', 'shorten_url': ''}
            return render_template('index.html', data = params)

        # create unique shorten url
        while True:
            shorten_url = generate(size=7)

            # check that shorten url is not exist
            conn = sqlite3.connect('URL_Database.db')
            shorten_url_data = conn.execute("SELECT SHORTEN_URL FROM URLS WHERE SHORTEN_URL='{shorten_url}'")
            url_present_database = False
            for row in shorten_url_data:
                url_present_database = True
            conn.close()
            if url_present_database == False:
                break
        
        # create actual row
        conn = sqlite3.connect('URL_Database.db')
        conn.execute(f"INSERT INTO URLS (ORIGNAL_URL, SHORTEN_URL) VALUES ('{orignal_url}', '{shorten_url}')")
        conn.commit()
        conn.close()

        params = {'valid_check':'none', 'shorten_url': f'{config.URL_START + shorten_url}', 'orignal_url': f'{orignal_url}'}
            
        return render_template('index.html', data = params)

@app.route('/<string:shorten_link>')
def shorten_link(shorten_link):
    if request.method == 'GET' or request.method == 'POST':
        # check that shorten url exist or not
        conn = sqlite3.connect('URL_Database.db')
        shorten_url_data = conn.execute(f"SELECT SHORTEN_URL FROM URLS WHERE SHORTEN_URL='{shorten_link}'")
        link_present = False
        for row in shorten_url_data:
            link_present = True
        conn.close()

        # redirect if shorten link is present
        if link_present == True:
            # grab orignal link form database
            conn = sqlite3.connect('URL_Database.db')
            shorten_url_data = conn.execute(f"SELECT ORIGNAL_URL, SHORTEN_URL FROM URLS WHERE SHORTEN_URL='{shorten_link}'")
            for row in shorten_url_data:
                return redirect(row[0])
            conn.close()
        else:
            return render_template("404.html") 

@app.errorhandler(400) 
def not_found400(e): 
  return render_template("400.html") 

@app.errorhandler(404) 
def not_found404(e): 
  return render_template("404.html") 

@app.errorhandler(500) 
def not_found500(e): 
  return render_template("500.html") 


if __name__ == "__main__":
    app.run(debug=config.DEBUG)