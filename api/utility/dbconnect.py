import psycopg2
from api.utility.config import config
from werkzeug.security import generate_password_hash
from api.models.users import Users

user = Users.userdb
class Database():
 
    def __init__(self,conn=None):
        self.conn = conn  
        try:
            params = config() # read connection parameters from config file 
            self.conn = psycopg2.connect(**params) #connecting
            self.conn.autocommit = False
            #self.conn.setAutoCommit(true);
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
            # create a cursor
            cur = self.conn.cursor() 
            # execute a statement in the sql file
            sql_file = open('api/models/db_queries.sql','r') 
            cur.execute(sql_file.read())
            # commit the changes
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def add_user(self,**user):
        try:           
            f_name = user['firstname']
            l_name =user['lastname']
            o_name = user['othername']
            email = user['email']
            p_number = user['phonenumber']
            u_name = user['username']
            p_word = generate_password_hash(user['password'], method='sha256')
            is_admin = user.get('isadmin')
            
            #check if user doesn't exist
            user_exist = self.check_user_is_unique(**user)
            print("user exists status {} ".format(user_exist))
            if type(user_exist) is int: 
                script = """
                            INSERT INTO users (firstname,lastname,othername,email,phonenumber,username,password,isadmin)
                            VALUES ('{}','{}','{}','{}','{}','{}','{}',{})

                        """.format(f_name,l_name,o_name,email,p_number,u_name,p_word,is_admin) 
                params = config() # read connection parameters from config file 
                self.conn = psycopg2.connect(**params) #connecting
                cur = self.conn.cursor()
                cur.execute(script) 
                self.conn.commit() 
                return "success"
            else:
                return(user_exist)
        except (Exception, psycopg2.DatabaseError) as error:
            if "email" in str(error):
                return "Email already exists"   
            elif "username" in str(error):
                return "Username already exist"
            elif "phonenumber" in str(error):
                return "Phone Number already exist"
            else:
                print("Create User Error >> {}".format(error))
                return "error occured contact admin"
    def get_user():
        pass
    def check_user_is_unique(self, **user):
        try: 
            email = user['email']
            p_number = user['phonenumber']
            u_name = user['username'] 
            script = """
                        SELECT * FROM users WHERE email = '{}' OR phonenumber= '{}' OR username = '{}'
                    """.format(email,p_number,u_name) 
            params = config() # read connection parameters from config file 
            self.conn = psycopg2.connect(**params) #connecting
            cur = self.conn.cursor()
            cur.execute(script)
            result = cur.rowcount
            self.conn.rollback() 
            cur.close 
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def add_incident(self,**incident):
        try: 
            i_title = incident['title']
            i_type = incident['type']
            i_comment =incident['comment']
            i_status = incident['status']
            i_createdby = incident['createdby'] 
            i_location = incident['location']  
            script = """
                        INSERT INTO incidents (title,type,comment,status,createdby,location)
                        VALUES (%s,%s,%s,%s,%s,%s);
                    """ 
            params = config() # read connection parameters from config file 
            self.conn = psycopg2.connect(**params) #connecting
            cur = self.conn.cursor()
            cur.execute(script,(i_title,i_type,i_comment,i_status,i_createdby,i_location))
            self.conn.commit()
            cur.close
            return "success";
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return("Not created")
    def get_incident():
        pass 
    def get_all_incidents():
        pass
    def update_incident(self,what_to_update,user_id,update_with):
        #what_to_update can be location, comment or status
        try: 
            script = """
                        UPDATE incidents SET {} = '{}' WHERE id = '{}';
                    """ .format(what_to_update,update_with,user_id)
            params = config() # read connection parameters from config file 
            self.conn = psycopg2.connect(**params) #connecting
            cur = self.conn.cursor()
            cur.execute(script)
            self.conn.commit()
            cur.close
            return "success";
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return("Not created")
        pass
    def delete_incident():
        pass
        