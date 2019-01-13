import datetime,json
from werkzeug.security import generate_password_hash
class Users:
    userdb =[
    {
        "id": 1, #integer
        "firstname" : "Alex",
        "lastname" : "Ssanya",
        "othername" : "",
        "email" : "alexxsanya@gmail.com",
        "phonenumber" : "+256702342257",
        "username" : "alexxa",
        "password": generate_password_hash('uganda256', method='sha256'),
        "registered" : str(datetime.datetime.now()), #TimeTamp
        "isAdmin" : False # Boolean
    }
]