import psycopg2
from api.utility.config import config
from api.models.users import Users

user = Users.userdb
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
                    password varchar(250) NOT NULL,
                    isadmin BOOLEAN NOT NULL,
                    registered TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
    def add_user(self,user):
        try:
            user = user[0]
            
            f_name = user['firstname']
            l_name =user['lastname']
            o_name = user['othername']
            email = user['email']
            p_number = user['phonenumber']
            u_name = user['username']
            p_word = user['password']
            is_admin = user['isadmin']
            print(f_name)
            script = """
                        INSERT INTO users (firstname,lastname,othername,email,phonenumber,username,password,isadmin)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
                    """
            cur = self.conn.cursor()
            cur.execute(script,(f_name,l_name,o_name,email,p_number,u_name,p_word,is_admin))
            self.conn.commit()
            cur.close
            print("user has been successfully added")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def get_user():
        pass
    def add_incident(self,**incident):
        try:
            print(incident) 
            i_title = incident['title']
            i_type = incident['type']
            i_comment =incident['comment']
            i_status = incident['status']
            i_createdby = incident['createdby'] 
            i_location = incident['location'] 

            script = """INSERT INTO incidents (title,type,comment,status,createdby,location)
                        VALUES (%s,%s,%s,%s,%s,%s);
                    """
            cur = self.conn.cursor()
            cur.execute(script,(i_title,i_type,i_comment,i_status,i_createdby,i_location))
            self.conn.commit()
            cur.close
            print("Incident has been successfully created")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
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
        