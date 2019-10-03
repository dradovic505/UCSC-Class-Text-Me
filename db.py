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
        user_phone = { 'phone': phone }
        new_id = { '$set': { 'user_id': user_id } }
        self.my_table.update_one(user_phone, new_id)

    def get_user(self, user_id):
        user = self.my_table.find_one({'user_id':user_id})
        return user

    def set_availability(self, user_id, class_name, availability):
        user = self.my_table.find_one({'user_id':user_id})
        new_class_availability = {'class_name':class_name, 'previously_open':availability}
        old_class_list = user['class_list']
        new_class_list = []
        for c in old_class_list:
            if c['class_name'] != class_name:
                new_class_list.append(c)
            else:
                new_class_list.append(new_class_availability)
        new_availability = { '$set': { 'class_list' : new_class_list } }
        self.my_table.update_one(user_id, new_availability)
        print('hello there')
        print(self.my_table.find_one({'user_id':user_id}))
        
    def print_db(self):
        for x in self.my_table.find():
            print(x)
