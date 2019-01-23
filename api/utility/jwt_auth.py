import os, datetime 
from functools import wraps
from flask import g, request, url_for, jsonify,Flask
import jwt

class Auth():
    def __init__(self,username=""):
        self.username = username
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
                    'status':401,
                    'message':"Only Admins are unauthorized to access this page"
                })          
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def encode_token(user_name,isadmin):  
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=30, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_name,
                'isadmin':isadmin
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
            payload = jwt.decode(token, 'secretme', algorithms=['HS256'])
            return payload['sub']
        except (Exception, jwt.exceptions.DecodeError) as error:
            #raise error
            pass   
    def is_admin_check(self,token):
        try:
            payload = jwt.decode(token, "secretme")
            return payload['isadmin']
        except Exception as error:
            return error