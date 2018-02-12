import sqlite3


class sqldb:

    def __init__(self, db):
        self.db = sqlite3.connect('sqlite_db/'+db)
        # self.create_member_table()

    def create_member_table(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE members(id INTEGER PRIMARY KEY, firstname TEXT,
            middlename TEXT, lastname TEXT, dob TEXT, birthplace TEXT)
        ''')
        self.db.commit()

    def db_member_registration(self, firstname, middlename, lastname, dob, birthplace):
        cursor = self.db.cursor()
        try:
            cursor.execute('''
                INSERT INTO members(firstname, middlename, lastname, dob, birthplace) VALUES (?, ?, ?, ?, ?)
            ''', (firstname, middlename, lastname, dob, birthplace))
            success = True
        except Exception as e:
            print(str(e))
            success = False

        print('First User inserted')
        self.db.commit()

        return success

    def fetch_db_members(self):
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                          SELECT firstname, middlename, lastname, dob, birthplace FROM members
                          ''')
            firstnames = []
            middlenames = []
            lastnames = []
            dobs = []
            birthplaces = []
            all_rows = cursor.fetchall()
            for row in all_rows:
                firstnames.append(str(row[0]))
                middlenames.append(str(row[1]))
                lastnames.append(str(row[2]))
                dobs.append(str(row[3]))
                birthplaces.append(str(row[4]))

            cursor.close()

            return firstnames, middlenames, lastnames, dobs, birthplaces
        except Exception as error:
            print(str(error))