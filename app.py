#Python3
#source env/bin/activate
from flask import Flask, render_template, request, redirect, escape, url_for
from jinja2 import utils
import ast
from db import UserDB
from find_classes import Scraper

#app calls database to enter user's info and which classes he wants
    #to get notified for.
#every x minutes, app calls find_classes to get the seats and
    #waitlist for each class. app calls database to get user's
    #telegram number, uses telegram bot to send seats+waitlist for
    #each class to the user

# user_arr = [
#             {'name':'Bob', 'telegram':'(555)-555-5555',
#              'class_name':'STAT 5'},
# ]

app = Flask(__name__)

dbase = UserDB()
scraper = Scraper()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_info = request.form.to_dict()

        #escaping to prevent XSS attack
        new_name = str(utils.escape(user_info['name']))
        new_telegram = str(utils.escape(user_info['telegram']))
        new_class = str(utils.escape(user_info['class']))
        new_user = {'name':new_name, 'telegram':new_telegram, 'class':new_class}

        dbase.enter_data(user_info)
        return redirect(url_for('results',user_info=new_user))

    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    d = request.args.to_dict()
    user = d['user_info']
    user_info = ast.literal_eval(user)

    if request.method == 'POST':
        if request.form['home'] == "Home":
            return redirect('/')

    if user_info:
        get_class_info()
        return render_template('results.html', user_info=user_info)

    return render_template('results.html')

def get_class_info():
    #for all people in database, find the class info
    user = dbase.return_data('Bob Dylan')
    d = scraper.find_info(user['class'])
    print(d)
    scraper.close_browser()

if __name__ == '__main__':
    app.run(debug=True)
