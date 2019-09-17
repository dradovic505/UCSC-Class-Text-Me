#Python3
#source env/bin/activate
from flask import Flask, render_template, request, redirect, escape, url_for
from jinja2 import utils
import ast
#import yaml

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

db = UserDB()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_info = request.form.to_dict()
        #escaping to prevent XSS attack
        # user_name = str(utils.escape(user_info['name']))
        # user_telegram = str(utils.escape(user_info['telegram']))
        # user_class = str(utils.escape(user_info['class']))
        user_info['name'] = str(utils.escape(user_info['name']))
        user_info['telegram'] = str(utils.escape(user_info['telegram']))
        user_info['class'] = str(utils.escape(user_info['class']))
        #put in database
        db.enter_data(user_info)
        return redirect(url_for('results',user_info=user_info))

    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    d = request.args.to_dict()
    user = d['user_info']
    user_info = ast.literal_eval(user)

    if request.method == 'POST':
        if form['home'] == "Home":
            return redirect('/')

    if user_info:
        return render_template('results.html', user_info=user_info)

    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
