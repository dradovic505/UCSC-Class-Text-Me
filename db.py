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
        name = u['name']
        same_name = self.my_table.find({'name':name})

        if not same_name:
            self.my_table.insert_one(u)

        # for x in self.my_table.find():
        #     print(x)

    #return user info from db
    def return_data(self, user_name):
        users_with_name = self.my_table.find({'name':user_name})
        user_dict = {}
        for user in users_with_name:
            user_dict['name'] = user['name']
            user_dict['telegram'] = user['telegram']
            user_dict['class'] = user['class']
        return user_dict
