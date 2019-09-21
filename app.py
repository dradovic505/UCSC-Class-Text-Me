#Python3
from flask import Flask, render_template, request, redirect, escape, url_for
from jinja2 import utils
import ast, schedule, time, threading
from db import UserDB
# from telegram_bot import TelegramBot
from find_classes import Scraper

# database structure = [{'name':'', 'telegram':'', 'class_name':''}]

app = Flask(__name__)
dbase = UserDB()
scraper = Scraper()
# bot = TelegramBot()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_info = request.form.to_dict()
        #escaping to prevent XSS attack
        new_name = str(utils.escape(user_info['name']))
        new_phone = str(utils.escape(user_info['phone']))
        new_class = str(utils.escape(user_info['class']))
        new_user = {'name':new_phone, 'telegram':new_phone, 'user_id':-1,
                    'send_messages':True, 'class':new_class}
        dbase.enter_data(user_info)
        return redirect(url_for('unverifiedUser',user_info=new_user))

    return render_template('index.html')

@app.route('/unverifiedUser', methods=['GET', 'POST'])
def unverifiedUser():
    # d = request.args.to_dict()
    # user = d['user_info']
    # user_info = ast.literal_eval(user)

    if request.method == 'POST':
        if request.form['home'] == "Home":
            return redirect('/')
    send_messages()
    return render_template('unverifiedUser.html')

def access_bot(user):
    class_info = scraper.find_info(user['class'])
    scraper.close_browser()
    #send class_info to user as a telegram message
    if class_info[2] == '0':
        # bot.class_full(user['class'])
    return class_info

def run_threaded(job_func): #access_bot() is the job
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def send_messages():
    for user in dbase.return_all_verified_data():
        schedule.every(15).minutes.do(run_threaded, access_bot(user))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    app.run(debug=True)
