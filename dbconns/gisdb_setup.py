import psycopg2
from gisdb_config import config
from psycopg2.extensions import AsIs


class gisdb:

    def __init__(self):
        self.params = config()
        try:
            self.create_table()
        except Exception as error:
            print(str(error))
            pass

    def connect(self):
        conn = None
        try:
            print('Connecting to gisdb in Postgres environment...')
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
        command = (
            '''
            CREATE TABLE url_info_table (
             lat_long VARCHAR (255),
             city VARCHAR(255),
             region VARCHAR(255),
             country VARCHAR(255),
             ip VARCHAR(255) NOT NULL PRIMARY KEY,
             org VARCHAR(255))
            ''')

        conn = None
        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            cur.execute(command)
            print('Member table has been created...')
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(str(error))
        finally:
            if conn is not None:
                conn.close()


    # def insertDictData(self, data):
    #     result = False
    #     for d in data:
    #         columns = d.keys()
    #         values = [d[column] for column in columns]
    #
    #         insert_statement = 'insert into url_info_table (%s) values %s'
    #         print(insert_statement)
    #         conn = None
    #         try:
    #
    #             conn = psycopg2.connect(**self.params)
    #             cur = conn.cursor()
    #             cur.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    #             print('data has been inserted')
    #             cur.close()
    #             conn.commit()
    #             result = True
    #         except (Exception, psycopg2.DatabaseError) as error:
    #             print(str(error))
    #             if conn:
    #                 conn.rollback()
    #         finally:
    #             if conn is not None:
    #                 conn.close()
    #
    #     return result



    def insertDictData(self, data):
        err = ''
        # print('URL INFORMATION GIS')
        # print(data)
        sql = '''
        INSERT INTO url_info_table(lat_long, city, region, country, ip, org)
        VALUES (%(loc)s, %(city)s, %(region)s, %(country)s, %(ip)s, %(org)s)
        '''

        conn = None
        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()
            cur.executemany(sql, data)
            print('url has been inserted...')
            success = True
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            err = error
            if conn:
                conn.rollback()
            success = False
        finally:
            if conn is not None:
                conn.close()

        return success, err
