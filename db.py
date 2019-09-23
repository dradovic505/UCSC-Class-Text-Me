import pymongo, yaml
from pymongo import MongoClient

# my_credentials = yaml.safe_load(open('db.yaml'))
# db_name = my_credentials['my_db']
# my_client = MongoClient()
# my_db = my_client[db_name]
# my_table = my_db['users']
# my_table.drop()

class UserDB:

    def __init__(self):
        self.my_credentials = yaml.safe_load(open('db.yaml'))
        self.db_name = self.my_credentials['my_db']
        self.my_client = MongoClient()
        self.my_db = self.my_client[self.db_name]
        self.my_table = self.my_db['users']

    def enter_data(self, u):
        phone = u['phone']
        same_phone = self.my_table.find_one({'phone':phone})

        if not same_phone:
            print('query entered')
            self.my_table.insert_one(u)

    def add_user_id(self, phone, user_id):
        user_phone = { "phone": phone }
        new_id = { "$set": { "user_id": user_id } }
        self.my_table.update_one(user_phone, new_id)

    #returns all user data for verified users who still want messages
    def return_all_verified_data(self):
        user_arr = []
        for user in self.my_table.find():
            user_dict = {}
            if user['user_id'] != -1 and user['send_messages']:
                user_dict['name'] = user['name']
                user_dict['phone'] = user['phone']
                user_dict['user_id'] = user['user_id']
                user_dict['class'] = user['class']
            user_arr.append(user_dict)
        return user_arr

    def print_db(self):
        for x in self.my_table.find():
            print(x)
