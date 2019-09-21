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
        # user_id = u['user_id']
        phone = u['phone']
        # same_id = self.my_table.find({'user_id':user_id, 'phone':phone})
        same_id = self.my_table.find({'phone':phone})

        if not same_id:
            self.my_table.insert_one(u)

        for x in self.my_table.find():
            print(x)

    def add_user_id(self, phone, user_id):
        self.my_table.update({'phone':phone}, {'user_id':user_id})
        for x in self.my_table.find():
            print(x)

    #return user info from db
    def return_data(self, phone_number, user_id):
        user_with_phone = self.my_table.find({'phone_number':phone_number, 'user_id':user_id})

        if user_id == '':
            #return emtpy dict, can't show data until user is verified
            return []

        user_dict = {}
        for user in user_with_phone:
            user_dict['name'] = user['name']
            user_dict['phone'] = user['phone']
            user_dict['user_id'] = user['user_id']
            user_dict['class'] = user['class']
        return user_dict
