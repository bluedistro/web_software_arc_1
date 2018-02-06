import pymongo
from pymongo import MongoClient
import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class User():

    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


class database:

    def __init__(self, database, user_collection):

        self.client = MongoClient()
        self.database = self.client[database]
        self.users = self.database[user_collection]


    def register_user(self, firstname, lastname, email, password):
        success = False
        password_hash = generate_password_hash(password)
        user_info = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password_hash
        }
        user_id = self.users.insert_one(user_info).inserted_id

        if user_id != None:
            success = True
        return user_id, success
