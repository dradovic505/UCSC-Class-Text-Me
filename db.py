import pymongo, yaml
from pymongo import MongoClient

class UserDB:

    def __init__(self):
        self.my_credentials = yaml.safe_load(open('db.yaml'))
        self.db_name = self.my_credentials['my_db']
        self.my_client = MongoClient()
        self.my_db = self.my_client[self.db_name]
        self.my_table = self.my_db['users']

    #enter user info into db
    def enter_data(self, u):
        phone = u['phone']
        same_phone = self.my_table.find({'phone':phone})

        if not same_phone:
            self.my_table.insert_one(u)

    def add_user_id(self, phone, user_id):
        self.my_table.update({'phone':phone}, {'user_id':user_id})
        for x in self.my_table.find():
            print(x)

    #returns all user data for verified users who still want messages
    def return_all_verified_data(self):
        user_dict = {}
        for user in self.my_table.find():
            if user['user_id'] != -1 and user['send_messages']:
                user_dict['name'] = user['name']
                user_dict['phone'] = user['phone']
                user_dict['user_id'] = user['user_id']
                user_dict['class'] = user['class']
        return user_dict
