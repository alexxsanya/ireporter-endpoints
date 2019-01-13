from flask import jsonify, make_response, abort 
from api.models.users import Users
import re
users  = Users.userdb 
class UserValidator:
    def __init__(self):
        pass
    @staticmethod
    def validate_user(input_name, input_value, return_value):
        if input_value == "" or type(input_value) is int:
            abort(make_response(jsonify({
                "status": 400,
                "error": return_value
            }), 400))
        else:
            if input_name == "email": 
                email_regex = re.compile(r'''([a-zA-Z0-9._%+-]+@ [a-zA-Z0-9.-]+ (\.[a-zA-Z]{2,4}))''', re.VERBOSE)
                valid_email = email_regex.search(input_value)
                if not valid_email:
                    abort(make_response(jsonify({
                        "status": 400,
                        "error": "email must be of the form (user@domain.xxx)"
                    }), 400))  

                for user in users: 
                    if user['email'] == input_value: 
                        abort(make_response(jsonify({
                            "status": 400,
                            "error": "The Supplied Email Address already exists"
                        }), 400))  

            elif input_name == "phonenumber":
                #ensure that no character is persent in the supplied number
                try:
                    print(int(input_value))
                except ValueError:
                    abort(make_response(jsonify({
                        'status': 400,
                        'error': "Phone number should only contain digits"
                    }), 400))                    
                if len(str(input_value)) != 12:
                    abort(make_response(jsonify({
                        'status': 400,
                        'error': "Phone number should have 12 digits"
                    }), 400))

                phone = re.compile(r'''( 256?(\d{3})(\d{6}) )''', re.VERBOSE)
                valid_phone_number = phone.search(input_value)
                if not valid_phone_number: 
                    abort(make_response(jsonify({
                        'status': 400,
                        'error': "Enter valid phone number eg (256 *** *** ***) like (256788111222)"
                    }), 400)) 

    @staticmethod
    def validate_login(user_input, return_value):
        if user_input == '':
            abort(make_response(jsonify({
                "status": 400,
                "error": return_value
            }), 400))