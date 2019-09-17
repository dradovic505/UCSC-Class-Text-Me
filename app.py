#Python3
#source env/bin/activate
from flask import Flask, render_template, request, redirect, escape, url_for
from jinja2 import utils
import ast
#import yaml

app = Flask(__name__)


#if user puts information into website, put in MongoDB database

# user = {}
# user[name] = {
#                 'telegram':'',
#                 'class_name':{
#                                'available_seats':_,
#                                'waitlist':_
#                              }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_info = request.form.to_dict()
        #escaping to prevent XSS attack
        user_name = str(utils.escape(user_info['name']))
        user_telegram = str(utils.escape(user_info['telegram']))
        user_class = str(utils.escape(user_info['class']))
        #put in database

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
