from flask import Blueprint,jsonify, request, Response,g
import datetime,json 
from api.utility.validate_incident import IncidentValidator
from api.utility.validate_user import UserValidator
from werkzeug.security import generate_password_hash, check_password_hash
from api.utility.jwt_auth import Auth
from api.utility.queries import DB_Queries

bluep = Blueprint("bluep", __name__)
incidentValidator = IncidentValidator()
userValidator = UserValidator()
db = DB_Queries() 
auth = Auth()

@bluep.route('/admin/signup', methods = ['POST'])
@bluep.route('/user', methods = ['POST'])
def create_user():  
    user_data_object = request.get_json()
    rule = request.url_rule
    if("admin" in rule.rule):
        token = request.headers.get('authorization')
        is_admin = auth.is_admin_check(token) 
        if is_admin == True:
            user_data_object['isadmin'] = True
        else:
            return jsonify({
                'status':401,
                'message':"Only Admins are unauthorized to access this page"
            })   
    else:
        user_data_object['isadmin'] = False
    to_validate = [ ["firstname", "Firstname is required & must be a string" ],
                ["lastname", "Lastname is required"],
                ["othername", "Othernames is required and must be a string"],
                ["username", "Username must be provided required with atleast 4 characters"],
                ["email" , "A valid email must be supplied as user@domain.xxx"],
                ["password","Password is required and should be atleast 8 characters"],
                ["phonenumber", "Phone number is required and must only contain digits"]
            ]
    for item in to_validate:
       #print(item[0] + " -> "+ item[1])
       userValidator.validate_user(item[0],user_data_object[item[0]], item[1])

    if not user_data_object['password']  or len(user_data_object['password']) < 8:
            return jsonify({
                "status": 400,
                "error": "Password is required & must be atleast 8 characters"
            }), 400

    query_status = db.add_user(**user_data_object)  
    if(query_status == "success"):
        g.user = user_data_object["username"]
        access_token = auth.encode_token(user_data_object['username'],user_data_object['isadmin']) 
        return Response(json.dumps({
            "status" : 201,
            "comment": "User - "+ str(user_data_object['username']) +"has been created",
            "access_token": access_token.decode('utf-8')
        }), 201, mimetype="application/json")  
    else:
        return jsonify({
            'status':400,
            'message': query_status
        })

@bluep.route('/admin/user/<int:user_id>', methods=['DELETE'])
@auth.jwt_required
@auth.admin_only
def delete_user(user_id):
    query_status = db.delete_user(user_id)
    if query_status > 0:
        return jsonify({'status':200,'id':user_id,'message':"The user has been deleted successfully"}) 
    else:
        return jsonify({'status':200 ,'id':user_id,'message':'No record found with the provided id'})    

@bluep.route("/admin/allusers",methods=['GET'])
@auth.jwt_required
@auth.admin_only
def get_all_users():
    users = db.get_all_user()
    if len(users) <= 0:
        return jsonify({
            "Status": 400,
            "error": "No users records in the database yet"
        }), 400
    else:
        return jsonify({'status':200,'data': users})

@bluep.route('/login', methods = ['POST'])
def login_user():
    data = request.get_json() 
    username = data['username']
    password = data['password']
    userValidator.validate_login(username, "username is required")
    userValidator.validate_login(password, "Password has not been supplied")
    login_status = db.login_user(**data) 
    print(login_status)
    if "failed" not in login_status:
        auth.username = login_status['username'] 
        #<username,isadmin>
        access_token = auth.encode_token(login_status['username'],login_status['isadmin']) 
        return jsonify({
                "status": 200,
                "status": "Login successful",
                "access_token": access_token.decode("utf-8")
            }), 200
    return jsonify({"status": 400, "error": "Invalid username or password"}), 400

@bluep.route('/redflags', methods=['GET'])
@auth.jwt_required
def get_all_red_flags(): 
    incidents = db.get_all_incidents()
    if len(incidents) <= 0:
        return jsonify({
            "Status": 400,
            "error": "No incident records in the database yet"
        }), 400
    else:
        return jsonify({'status':200,'data': incidents})

@bluep.route('/redflags/<int:red_flag_id>', methods = ['GET'])
@auth.jwt_required
def get_this_red_flag(red_flag_id):   
    query_status = db.get_incident(red_flag_id)  
    if query_status != None:
        return jsonify({'status':200,'data': query_status}) 
    else:
        return jsonify({'status':400,'message':"No data found for the provided ID"})    

@bluep.route('/redflags', methods = ['POST'])
@bluep.route('/intervention', methods = ['POST'])
@auth.jwt_required
def create_flag(): 
    redflag_data = request.get_json()

    rule = request.url_rule
    if("redflags" in rule.rule):
        redflag_data['type'] = "red-flag"
    else:
        redflag_data['type'] = "intervention"

    if (incidentValidator.validate_incident(redflag_data)):
        query_status = db.add_incident(**redflag_data)
        if(query_status == "success"): 
            return jsonify({
                    "status": 201,
                    "message": "Incident has been created", 
                }), 20
        else:
            return jsonify({
                'status':400,
                'message': query_status
            }) 

@bluep.route('/admin/incident/status/<int:red_flag_id>', methods = ['PATCH'])
@bluep.route('/redflags/<int:red_flag_id>/comment', methods = ['PATCH'])
@bluep.route('/redflags/<int:red_flag_id>/location', methods = ['PATCH'])
@auth.jwt_required
def update_incident(red_flag_id):
    request_data = request.get_json()
    rule = request.url_rule
    if("comment" in rule.rule):
        what_to_update = "comment"
    elif("location" in rule.rule):
        what_to_update = "location"
    elif("status" in rule.rule):
        what_to_update = "status"
        token = request.headers.get('authorization')
        is_admin = auth.is_admin_check(token) 
        if is_admin == True:
            user_data_object['isadmin'] = True
        else:
            return jsonify({
                'status':401,
                'message':"Only Admins are unauthorized to access this page"
            })  
    
    if (what_to_update in request_data and len(request_data[what_to_update]) > 5 ):
        #(self,what_to_update,user_id,update_with):
        d_status = db.update_incident(what_to_update,red_flag_id,request_data[what_to_update])

        if(d_status):
            return jsonify({
            'status':200,
            'comment': "The {} has been updated successfully".format(what_to_update)
            })
        else:
            return jsonify({
                'status':200,
                'comment': "{} not updated, No Incident record found with provided id {}".format(what_to_update,red_flag_id), 
                'tip':'cross-check the user id'
            })
    else:
        return jsonify({
            'status':200,
            'comment': "{} has not been modified".format(what_to_update), 
            'tip':'cross-check the user id'
        })

@bluep.route('/redflags/<int:flag_id>', methods = ['DELETE'])
@bluep.route('/intervention/<int:flag_id>', methods = ['DELETE'])
@auth.jwt_required
def delete_red_flag(flag_id):
    query_status = db.delete_incident(flag_id)
    if query_status > 0:
        return jsonify({'status':200,'id':flag_id,'message':"The record has been deleted successfully"}) 
    else:
        return jsonify({'status':200 ,'id':flag_id,'message':'No record found with the provided id'})       

@bluep.app_errorhandler(404)
def resource_not_found(error):
    message={
            "error":"Resource not found on the system",
            "info":"visit resource documentation"
        }
    return jsonify({
        "status":404,
        "message":"message"
    })

@bluep.app_errorhandler(500)
def sys_error_found(error):
    message={
            "error":"Resource not found on the system",
            "info":"visit resource documentation"
        }
    return jsonify({
        "status":404,
        "message":"message"
    })

@bluep.app_errorhandler(403)
def sys_error_found(error):
    message={
            "error":"Permission Error",
            "info":"Login as admin"
        }
    return jsonify({
        "status":404,
        "message":"message"
    })