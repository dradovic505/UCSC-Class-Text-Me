import pymongo, yaml
from pymongo import MongoClient

class UserDB:

    def __init__(self):
        my_credentials = yaml.safe_load(open('db.yaml'))
        db_name = my_credentials['my_db']
        myclient = MongoClient()
        mydb = myclient[db_name]
        my_table = mydb['users']

    #enter user info into db
    def enter_data(u):
        my_table.insert_one(u)

    #return user info from db
    def return_data(user_name):
        users_with_name = my_table.find({'name':user_name})
        user_dict = {}
        for user in users_with_name:
            user_dict['name'] = user['name']
            user_dict['telegram'] = user['telegram']
            user_dict['class'] = user['class']
        return user_dict
