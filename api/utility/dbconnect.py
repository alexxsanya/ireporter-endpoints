import psycopg2
from api.utility.config import config
class Database():
 
    def __init__(self,conn=None):
        self.conn = conn  
        try:
            params = config() # read connection parameters from config file 
            self.conn = psycopg2.connect(**params) #connecting
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
 
    def close_connection(self):
        try:
            if self.conn is not None:
                self.conn.close()
                print('database connection closed successfully.')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def create_tables(self): 
        # create a cursor
        cur = self.conn.cursor() 
        # execute a statement 
        cur.execute('SELECT version()')
        # display the PostgreSQL database server version
        db_version =   cur.fetchone()
        print(db_version) 
        cur.close()
    def add_user():
        pass
    def get_user():
        pass
    def add_incident():
        pass
    def get_incident():
        pass
    def get_all_incidents():
        pass
    def update_incident():
        #update status by admin
        #update comment by user
        #update location by user
        pass
    def delete_incident():
        pass