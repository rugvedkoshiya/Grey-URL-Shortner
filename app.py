from flask import Flask, render_template, request, redirect
import sqlite3
import validators
import random
# import base64

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
        if valid_check == True:
            pass
        else:
            params = {'valid_check':'block', 'orignal_url': f'{orignal_url}', 'shorten_url': ''}
            return render_template('index.html', data = params)


        alphabat = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                    '0','1','2','3','4','5','6','7','8','9']

        # create unique shorten url
        while True:
            shorten_list = random.sample(alphabat, 5)
            shorten_url = ''
            for i in shorten_list:
                shorten_url += ''.join(i)

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

        params = {'valid_check':'none', 'shorten_url': f'https://greyshortner.herokuapp.com/{shorten_url}', 'orignal_url': f'{orignal_url}'}
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
    app.run(debug=False)