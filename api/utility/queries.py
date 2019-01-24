from api.utility.dbconnect import Database 
from werkzeug.security import generate_password_hash,check_password_hash
import psycopg2

class DB_Queries():
    def __init__(self):
        self.cursor = Database().cur
        self.conn = Database().conn
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
            #print("user exists status {} ".format(user_exist))
            if type(user_exist) is int: 
                script = """
                            INSERT INTO users (firstname,lastname,othername,email,phonenumber,username,password,isadmin)
                            VALUES ('{}','{}','{}','{}','{}','{}','{}',{})

                        """.format(f_name,l_name,o_name,email,p_number,u_name,p_word,is_admin)   
                cursor.execute(script) 
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
    def get_all_user(self):
        try: 
            script = """
                        SELECT firstname,lastname,othername,email,registered,username FROM users;
                    """
            self.cursor.execute(script) 
            return self.cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return [str(error)]
    def delete_user(self,user_id): 
        try: 
            script = """
                        DELETE FROM users WHERE id ='{}';
                    """ .format(user_id) 
            self.cursor.execute(script)
            rows_deleted = self.cursor.rowcount   
            return rows_deleted;
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)     
    def check_user_is_unique(self, **user):
        try: 
            email = user['email']
            p_number = user['phonenumber']
            u_name = user['username'] 
            script = """
                        SELECT * FROM users WHERE email = '{}' OR phonenumber= '{}' OR username = '{}'
                    """.format(email,p_number,u_name) 
            self.cursor.execute(script) 
            result = self.cursor.rowcount
            self.conn.rollback()  
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
            self.cursor.execute(script,(i_title,i_type,i_comment,i_status,i_createdby,i_location))
            return "success";
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return("Not created")
    def get_incident(self,incident_id):
        try: 
            script = """
                        SELECT * FROM incidents WHERE id = {}
                    """.format(incident_id) 
            self.cursor.execute(script)
            result = self.cursor.fetchone()
            self.conn.rollback()  
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("No data")
    def get_all_incidents(self):
        try: 
            script = """
                        SELECT * FROM incidents
                    """
            self.cursor.execute(script)
            result = self.cursor.fetchall()
            self.conn.rollback() 
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("No data")
    def update_incident(self,what_to_update,user_id,update_with):
        try: 
            script = """
                        UPDATE incidents SET {} = '{}' WHERE id = '{}';
                    """ .format(what_to_update,update_with,user_id)  
            self.cursor.execute(script)
            updated_rows = self.cursor.rowcount 
            if updated_rows == 1:
                result = True
            else:
                result = False 
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error) 
            return False
    def delete_incident(self,incident_id):
        try: 
            script = """
                        DELETE FROM incidents WHERE id ='{}';
                    """ .format(incident_id)
            self.cursor.execute(script)
            rows_deleted = self.cursor.rowcount 
            return rows_deleted;
        except (Exception, psycopg2.DatabaseError) as error:
            print(error) 
    def login_user(self,**user):
        password = user['password']  
        try: 
            script = """
                        SELECT username,password,isadmin,id FROM users WHERE username ='{}' OR email = '{}';
                    """ .format(user['username'],user['username'])
 
            self.cursor.execute(script) 
            data = self.cursor.fetchone()
            status = check_password_hash(data['password'], password)  
            if status: 
                return data
            return ["failed"]
        except (Exception, psycopg2.DatabaseError) as error:
            return ["{}".format(error),"failed"]
            print(error)