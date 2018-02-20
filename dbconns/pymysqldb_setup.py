from mysql import connector

class mysql:

    def __init__(self, db='gps'):
        self.user='kingsley'
        self.pwd = 'Kewl4life!'
        self.db = db
        self.host = '127.0.0.1'
        # self.cnx = mysql.connector.connect(user='kingsley', password='Kewl4life!',
        #                       host='127.0.0.1', database='gps')

        # cnx.close()

        try:
            self.create_table()
        except Exception as e:
            print(str(e))
            pass


    def create_table(self):
        command = (
            '''
                  CREATE TABLE members (
                  firstname char (100) NOT NULL ,
                  middlename char (100),
                  lastname char (100) NOT NULL,
                  dob char (100) NOT NULL,
                  birthplace char (100) NOT NULL)
            ''')

        try:
            cnx = connector.connect(user='kingsley', password='Kewl4life!',
                                          host='127.0.0.1', database='gps')
            cursor = cnx.cursor()
            cursor.execute(command)
            print('Table created!')
            cursor.close()
            cnx.commit()
        except Exception as e:
            print(str(e))
            print('error!!!')
            pass



    def db_member_registration(self, firstname, middlename, lastname, dob, birthplace):
        sql = '''
         INSERT INTO members VALUES(%s, %s, %s, %s, %s)
        '''
        try:
            cnx = connector.connect(user='kingsley', password='Kewl4life!',
                                          host='127.0.0.1', database='gps')
            cursor = cnx.cursor()
            cursor.execute(sql, (firstname, middlename, lastname, dob, birthplace))
            print('member successfully registered!')
            success = True
            cnx.commit()
            cursor.close()
        except Exception as e:
            print('error')
            print(str(e))
            success = False

        return success

    def fetch_db_members(self):
        try:
            cnx = connector.connect(user='kingsley', password='Kewl4life!',
                                          host='127.0.0.1', database='gps')
            cursor = cnx.cursor()
            sql = '''
                SELECT firstname, middlename, lastname, dob, birthplace FROM members
            '''
            cursor.execute(sql)
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
            print(firstnames)
            print(lastnames)
            return firstnames, middlenames, lastnames, dobs, birthplaces

        except Exception as e:
            print('Error retrieving data....')
            print(str(e))


# msl = mysql()
# msl.db_member_registration('Joseph', 'Obiri', 'Yeboah' ,'09/08/1945', 'Tamale')
# msl.fetch_db_members()
