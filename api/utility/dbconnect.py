import psycopg2
from psycopg2.extras import RealDictCursor
from api.utility.config import config
from os import environ
class Database():
    
    def __init__(self): 
        try:
            params = config() # read connection parameters from config file 
            env = environ.get("FLASK_ENV")
            db_url = environ.get("DATABASE_URL") 
            if(env == "production"):
                self.conn = psycopg2.connect(db_url) #connection for heroku
            else:
                self.conn = psycopg2.connect(**params) #connecting"""
            self.conn.autocommit = True
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.create_tables()
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
        try:
            # execute a statement in the sql file
            sql_file = open('api/models/db_queries.sql','r') 
            self.cur.execute(sql_file.read())
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
