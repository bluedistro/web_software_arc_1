import pymongo
import pymongo.errors
from pymongo import MongoClient
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class database:

    def __init__(self, db, user_collection):

        self.client = MongoClient()
        self.db = self.client[db]
        self.user_collection = user_collection
        self.users = self.db[self.user_collection]

    # user registration
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
        collection = self.db['users']
        cursor = collection.find({})
        for document in cursor:
            documents.append(document['email'])

        status = "Email has already been registered!, please use another email"
        message = [status for em in documents if unicode(email).lower() in em.lower()]
        return message

    # validation of user during login
    def login_user(self, email, password):
        emails_doc = []
        passwords_doc = []
        firstname_doc = []
        lastname_doc = []
        collection = self.db['users']
        cursor = collection.find({})
        for document in cursor:
            emails_doc.append(document['email'])
            passwords_doc.append(document['password'])
            firstname_doc.append(document['firstname'])
            lastname_doc.append(document['lastname'])
        user_firstname = ''
        user_lastname = ''
        for e, p, f, l in zip(emails_doc, passwords_doc, firstname_doc, lastname_doc):
            if e == unicode(email) and check_password_hash(p, unicode(password)) is True:
                print('found match')
                status = True
                if status:
                    user_firstname = str(f)
                    user_lastname = str(l)
                else:
                    user_firstname = ''
                    user_lastname = ''
                break
            else:
                print('Match not found')
                status = False


        return status, user_firstname, user_lastname

    def db_member_registration(self, firstname, middlename, lastname, dob, birthplace):
        success = False
        user_info = {
            'firstname': firstname,
            'middlename': middlename,
            'lastname': lastname,
            'dob': dob,
            'birthplace': birthplace
        }

        if firstname and lastname and dob and birthplace is not None:
            success = True
            user_id = self.users.insert_one(user_info).inserted_id
        else:
            success = False
            user_id = None

        return user_id, success

    def fetch_db_members(self):
        firstnames = []
        middlenames = []
        lastnames = []
        dobs = []
        birthplaces = []
        collection = self.db[self.user_collection]
        cursor = collection.find({})
        for document in cursor:
            firstnames.append(str(document['firstname']))
            middlenames.append(str(document['middlename']))
            lastnames.append(str(document['lastname']))
            dobs.append(str(document['dob']))
            birthplaces.append(str(document['birthplace']))
        return firstnames, middlenames, lastnames, dobs, birthplaces

    def fetch_detail_in_search(self, fname):
        collection = self.db[self.user_collection]
        cursor = collection.find({})
        firstnames = []
        for document in cursor:
            firstnames.append(str(document['firstname']))
        result = [fn for fn in firstnames if fname.lower() in fn.lower()]
        # print(result)
        return result


# db = database(db='bdr', user_collection='members')
# print(db.fetch_detail_in_search(fname='Dora'))
