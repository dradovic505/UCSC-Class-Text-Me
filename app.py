#Python3
#source env/bin/activate
from flask import Flask, render_template, request, redirect, escape, url_for
from jinja2 import utils
import ast
from db import UserDB
from find_classes import Scraper

# user_arr = [{'name':'', 'telegram':'', 'class_name':''}]

app = Flask(__name__)

dbase = UserDB()
scraper = Scraper()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_info = request.form.to_dict()

        #escaping to prevent XSS attack
        new_name = str(utils.escape(user_info['name']))
        new_phone = str(utils.escape(user_info['phone']))
        new_class = str(utils.escape(user_info['class']))
        new_user = {'name':new_phone, 'telegram':new_phone, 'user_id':0, 'class':new_class}

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
        get_class_info(user_info['phone'])
        return render_template('results.html', user_info=user_info)

    return render_template('results.html')

def get_class_info(user_id):
    #for all people in database, find the class info
    user = dbase.return_data(user_id)
    if user == []:
        return render_template('unverifiedUser.html')
    d = scraper.find_info(user['class'])
    return d
    scraper.close_browser()

def access_bot():
    #for each user, go through /start and /verifyNumber in the telegram bot
    #program. The bot will place their user id in the db.
    #here: every 15 minutes call get_class_info


if __name__ == '__main__':
    app.run(debug=True)
