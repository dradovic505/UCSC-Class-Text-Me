from flask import Flask, render_template, request, redirect, escape, url_for
from jinja2 import utils
import ast, schedule, time, threading
from db import UserDB

# database structure = [{'name':str, 
#                        'phone':int,
#                        'user_id':int, 
#                        'class_list':[
#                            {'class_name':str, 
#                             'previously_open':Bool
#                             }]
#                       }]

app = Flask(__name__)
dbase = UserDB()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_info = request.form.to_dict()
        #escaping to prevent XSS attack
        new_name = str(utils.escape(user_info['name']))
        inputted_phone = str(utils.escape(user_info['phone']))
        new_phone = inputted_phone.split('-')
        new_phone = '1' + ''.join(new_phone)
        new_class = str(utils.escape(user_info['class']))
        new_user = {'name':new_name, 
                    'phone':new_phone,
                    'user_id':-1, 
                    'class_list':[{'class_name':new_class, 'previously_open':False}]}
        dbase.enter_data(new_user)
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

    return render_template('unverifiedUser.html')

if __name__ == '__main__':
    app.run(debug=True)
