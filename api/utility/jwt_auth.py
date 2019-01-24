import os, datetime 
from functools import wraps
from flask import g, request, url_for, jsonify,Flask
import jwt
from os import environ

class Auth():
    def __init__(self,username=""):
        self.username = username
        self.secret_key = environ.get("SECRET_KEY")
    def jwt_required(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('authorization') 
            if token: 
                if str(token[:6]) == "Bearer": 
                    username_in_token = self.decode_token(token[7:].encode('utf-8'))
                    print(">>> {}".format(self.username))
                    if  username_in_token == self.username:
                        pass
                    else:
                        return jsonify({
                            "message":"Invalid Token, Sign in Again", 
                        })                        
                    
                else:
                    return jsonify({
                        "message":"Wrong Authorization Type used",
                        "info": "Use Bearer Token"
                    })
            else:
                return jsonify({
                    "error":"Missing Authorization Header"
                })            
            return f(*args, **kwargs)
        return decorated_function
    
    def admin_only(self,f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('authorization')
            is_admin = self.is_admin_check(token) 
            if is_admin == True:
                pass
            else:
                return jsonify({
                    'status':403,
                    'message':"Only Admins are unauthorized to access this page"
                })          
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def encode_token(user_name,isadmin,user_id):  
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user_name,
                'isadmin':isadmin,
                'is_id':user_id
            }
            return jwt.encode(
                payload,
                #app.config.get('SECRET_KEY'),
                "secretme",
                algorithm='HS256'
            )
        except Exception as error:
            return error

    def decode_token(self,token):
        try:

            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['sub']
        except (Exception, jwt.exceptions.DecodeError) as error:
            #raise error
            pass   
    def is_admin_check(self,token):
        try:
            payload = jwt.decode(token[7:].decode("utf-8"), self.secret_key, algorithms=['HS256'])
            return payload['isadmin']
        except Exception as error:
            return error
    def return_user_id(self,token):
        try:
            payload = jwt.decode(token[7:].decode("utf-8"), self.secret_key, algorithms=['HS256'])
            return payload['is_id']
        except Exception as error:
            return error        