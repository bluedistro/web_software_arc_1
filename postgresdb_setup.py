import psycopg2
from postgres_config import config


class pgdb:

    def __init__(self):
        self.params = config()

    def connect(self):
        ''' Connect to the PostgreSQL database server'''
        conn = None
        try:
            # self.params = config()
            print('Connecting to the PostgreSQL Database')
            conn = psycopg2.connect(**self.params)

            cur = conn.cursor()

            print('PostgreSQL Database version: ')
            cur.execute('SELECT version()')

            db_version = cur.fetchone()
            print(db_version)

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
        finally:
            if conn is not None:
                conn.close()
                print('Database Connection Closed')

    def create_table(self):
        '''create tables in nia database'''
        commands = (
            '''
                CREATE TABLE members (
                  member_id SERIAL PRIMARY KEY,
                  firstname VARCHAR(255) NOT NULL,
                  middlename VARCHAR(255),
                  lastname VARCHAR (255),
                  dob VARCHAR (255),
                  birthplace VARCHAR (255))
            ''')

        conn = None
        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            cur.execute(commands)
            print('Member table has been created...')
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
        finally:
            if conn is not None:
                conn.close()

    def db_member_registration(self, firstname, middlename, lastname, dob, birthplace):
        '''Insert a new member into the nia database'''
        sql = '''
                INSERT INTO members(firstname, middlename, lastname, dob, birthplace)
                 VALUES (%s, %s, %s, %s, %s) RETURNING member_id;'''

        conn = None
        member_id = None
        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            cur.execute(sql, (firstname, middlename, lastname, dob, birthplace))
            member_id = cur.fetchone()[0]
            print('Member successfully registered!')
            success = True
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            success = False
        finally:
            if conn is not None:
                conn.close()

        return member_id, success


    def fetch_db_members(self):
        '''query data from nia table'''
        conn = None
        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            cur.execute("SELECT firstname, middlename, lastname, dob, birthplace FROM members ORDER BY firstname")
            print('The number of parts: ', cur.rowcount)
            firstnames = []
            middlenames = []
            lastnames = []
            dobs = []
            birthplaces = []
            all_rows = cur.fetchall()
            for row in all_rows:
                firstnames.append(str(row[0]))
                middlenames.append(str(row[1]))
                lastnames.append(str(row[2]))
                dobs.append(str(row[3]))
                birthplaces.append(str(row[4]))
            cur.close()

            return firstnames, middlenames, lastnames, dobs, birthplaces

        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
        finally:
            if conn is not None:
                conn.close()
