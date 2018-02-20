import pymssql



class pms2ql :

    def __init__(self, db='gec'):
        self.host = 'localhost'
        self.username = 'SA'
        self.password = 'Kewl4life!'
        self.database = 'gec'

    def create_table(self):
        commands = (
            '''
                  CREATE TABLE members (
                  firstname VARCHAR (100) NOT NULL ,
                  middlename VARCHAR (100),
                  lastname VARCHAR (100) NOT NULL,
                  dob VARCHAR (100) NOT NULL,
                  birthplace VARCHAR (100) NOT NULL)
            ''')


        try:
            conn = pymssql.connect(self.host, self.username, self.password, self.database)
            cursor = conn.cursor()
            cursor.execute(commands)
            print('Table created')
            cursor.close()
            conn.commit()
        except Exception as error:
            print(str(error))
        finally:
            if conn is not None:
                conn.close()


    def db_member_registration(self, firstname, middlename, lastname, dob, birthplace):
        sql = '''
         INSERT INTO members VALUES(%s, %s, %s, %s, %s)
        '''
        try:
            conn = pymssql.connect(self.host, self.username, self.password, self.database)
            cursor = conn.cursor()
            cursor.execute(sql, (firstname, middlename, lastname, dob, birthplace))
            print('member successfully registered!')
            success = True
            conn.commit()
            cursor.close()
        except Exception as e:
            print('error')
            print(str(e))
            success = False
        finally:
            if conn is not None:
                conn.close()

        return success

    def fetch_db_members(self):
        try:
            conn = pymssql.connect(self.host, self.username, self.password, self.database)
            cursor = conn.cursor()
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
            return firstnames, middlenames, lastnames, dobs, birthplaces

        except Exception as e:
            print('Error retrieving data....')
            print(str(e))
