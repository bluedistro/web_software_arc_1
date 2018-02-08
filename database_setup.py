import pymongo
import pymongo.errors
from pymongo import MongoClient
import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class database:

    def __init__(self, database, user_collection):

        self.client = MongoClient()
        self.database = self.client[database]
        self.user_collection = user_collection
        self.users = self.database[self.user_collection]

    def register_user(self, firstname, lastname, email, password):
        success = False
        password_hash = generate_password_hash(password)
        user_info = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "password": password_hash
        }
        status = self.validate_email(email=email)
        if firstname and lastname and email and password is not None:
            if status is not "Email already exist!, please use another email":
                user_id = self.users.insert_one(user_info).inserted_id
            else:
                success = False
                user_id = None
                pass

        if user_id != None:
            success = True
        return user_id, success

    # temporal validation of email before entry for both live search and final entry
    def validate_email(self, email):
        documents = []
        collection = self.database['users']
        cursor = collection.find({})
        for document in cursor:
            documents.append(document['email'])

        status = "Email has already been registered!, please use another email"
        message = [status for em in documents if unicode(email).lower() in em.lower()]
        return message

    def login_user(self, email, password):
        emails_doc = []
        passwords_doc = []
        # password_enc = generate_password_hash('Kewl4life!')
        # decoded = check_password_hash(password_enc, password)
        collection = self.database['users']
        cursor = collection.find({})
        for document in cursor:
            emails_doc.append(document['email'])
            passwords_doc.append(document['password'])

        # data = zip(emails_doc, passwords_doc)
        # print(data)
        for e, p in zip(emails_doc, passwords_doc):
            if e == unicode(email) and check_password_hash(p, unicode(password)) is True:
                print('found match')
                status = True
                break
            else:
                print('Match not found')
                status = False


        return status

# db = database(database='wsa', user_collection='users')
# print(db.login_user('bineykingsley36@gmail.com', 'Kewl4life!'))
