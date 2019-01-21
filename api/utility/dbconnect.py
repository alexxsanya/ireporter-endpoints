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
        tables = (
            """
                CREATE TABLE IF NOT EXISTS users(
                    id serial PRIMARY KEY,
                    firstname varchar(25) NOT NULL,
                    lastname varchar(25) NOT NULL,
                    othername varchar(25),
                    email varchar(50) NOT NULL UNIQUE,
                    phonenumber varchar(12) NOT NULL UNIQUE,
                    username varchar(12) NOT NULL UNIQUE,
                    isadmin BOOLEAN NOT NULL
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS incidents(
                    id serial NOT NULL PRIMARY KEY,
                    createdon TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    createdby INT NOT NULL,
                    type varchar(25), 
                    location varchar(50) NOT NULL,
                    status varchar(12) NOT NULL UNIQUE,
                    comment varchar(12) NOT NULL UNIQUE,
                    FOREIGN KEY (createdby) REFERENCES users (id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS incidents_images(
                    owner INT NOT NULL,
                    filename CHARACTER VARYING(255) NOT NULL,
                    mime_type CHARACTER VARYING(255) NOT NULL,
                    file_data BYTEA NOT NULL, 
                    FOREIGN KEY (owner) REFERENCES incidents(id)
                )                
            """
        )

        try:
            # create a cursor
            cur = self.conn.cursor() 
            # execute a statement 
            for table in tables:
                cur.execute(table) 
            # commit the changes
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
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