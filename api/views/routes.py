from flask import Blueprint,jsonify, request, Response,g,abort
import datetime,json 
from api.utility.validate_incident import IncidentValidator
from api.utility.validate_user import UserValidator
from werkzeug.security import generate_password_hash, check_password_hash
from api.utility.jwt_auth import Auth
from api.utility.queries import DB_Queries
from api.utility.mail_server import send_mail_notification
bluep = Blueprint("bluep", __name__)

incidentValidator = IncidentValidator()

userValidator = UserValidator()

db = DB_Queries() 
auth = Auth()
incident_type = ["red-flag","intervention"]
updatable_fields = ["location","comment","status"]

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
                'status':403,
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
        
        access_token = auth.encode_token(user_data_object['username'],
                        user_data_object['isadmin'],
                        user_data_object["id"]) 
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

@bluep.route('/user/<int:user_id>', methods=['DELETE'])
@auth.jwt_required
@auth.admin_only
def delete_user(user_id):
    query_status = db.delete_user(user_id)
    if query_status > 0:
        return jsonify({'status':200,'id':user_id,'message':"The user has been deleted successfully"}) 
    else:
        return jsonify({'status':200 ,'id':user_id,'message':'No record found with the provided id'})    

@bluep.route("/allusers",methods=['GET'])
@auth.jwt_required
@auth.admin_only
def get_all_users():
    users = db.get_all_user()
    return users
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
    if "failed" not in login_status:
        auth.username = login_status['username'] 
        #<username,isadmin>
        access_token = auth.encode_token(login_status['username'],
                        login_status['isadmin'],
                        login_status["id"])  
        return jsonify({
                "status": 200,
                "status": "Login successful",
                "access_token": access_token.decode("utf-8")
            }), 200
    return jsonify({"status": 400, "error": "Invalid username or password"}), 400

@bluep.route('/<string:incident>', methods=['GET'])
@auth.jwt_required
def get_all_red_flags(incident): 
    if incident in incident_type:
        incidents = db.get_all_incidents(incident)
        if len(incidents) <= 0:
            return jsonify({
                "Status": 400,
                "error": "No incident records in the database yet"
            }), 400
        else:
            return jsonify({'status':200,'data': incidents})
    else:
        abort(400)

@bluep.route('/<string:incident>/<int:flag_id>', methods = ['GET'])
@auth.jwt_required
def get_this_red_flag(incident,flag_id): 
    if incident in incident_type:
        query_status = db.get_incident(flag_id,incident)  
        if query_status != None:
            return jsonify({'status':200,'data': query_status}) 
        else:
            return jsonify({'status':400,'message':"No data found for the provided ID"})  
    else:
        abort(404)  

@bluep.route('/<string:incident>', methods = ['POST'])
@auth.jwt_required
def create_flag(incident): 

    if incident in incident_type:
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
    else:
        abort(404)

@bluep.route('/<string:incident>/<int:red_flag_id>/<string:field_to_update>', methods = ['PATCH']) 
@auth.jwt_required
def update_incidents(incident,red_flag_id,field_to_update):
    if incident in incident_type and field_to_update in updatable_fields:
        request_data = request.get_json() 
        column = [column for column in updatable_fields if(column == field_to_update) ]
        column_to_update = "".join(column)
        token = request.headers.get('authorization') 
        if(column_to_update == "status"): 
            is_admin = auth.is_admin_check(token.encode("utf-8"))  
            if is_admin == False:
                return jsonify({
                    'status':403,
                    'message':"Only Admins are unauthorized to access this page"
                })  
        if (column_to_update in request_data):
            #(self,column_to_update,user_id,update_with):
            update_by = auth.return_user_id(token.encode("utf-8"))
            d_status = db.update_incident(column_to_update,red_flag_id,
                            request_data[column_to_update],
                            update_by
                            )
            print(d_status)
            if(int(d_status["updated_rows"]) == 1):
                if column_to_update == "status":
                    send_mail_notification(**d_status)
                return jsonify({
                'status':200,
                'comment': "The {} has been updated successfully".format(column_to_update)
                })
            else:
                return jsonify({
                    'status':200,
                    'comment': "{} not updated, No record found with provided id {}".format(column_to_update,red_flag_id), 
                })
        else:
            return jsonify({
                'status':200,
                'comment': "{} has not been modified".format(column_to_update), 
                'tip':'cross-check the user id'
            })
    else:
        abort(404)

@bluep.route('/<string:incident>/<int:flag_id>', methods = ['DELETE'])
@auth.jwt_required
def delete_red_flag(incident,flag_id):
    if incident in incident_type:
        query_status = db.delete_incident(flag_id)
        if query_status > 0:
            return jsonify({'status':200,'id':flag_id,'message':"The record has been deleted successfully"}) 
        else:
            return jsonify({'status':200 ,'id':flag_id,'message':'No record found with the provided id'}) 
    else:
        abort(404)      

@bluep.app_errorhandler(404)
def resource_not_found(error):
    message={
            "error":"Requested resource not found on the system",
            "info":"visit resource documentation"
        }
    return jsonify({
        "status":404,
        "message":message
    })

@bluep.app_errorhandler(400)
def bad_request(error):
    message={
            "error":"Bad request made",
            "info":"Check your request"
        }
    return jsonify({
        "status":400,
        "message":"message"
    })

@bluep.app_errorhandler(403)
def permission_denied(error):
    message={
            "error":"permission_denied",
            "info":"Admin privilege required"
        }
    return jsonify({
        "status":404,
        "message":"message"
    })

@bluep.app_errorhandler(405)
def method_not_allowed(error):
    message={
            "error":"Method Not Allowed",
            "info":"visit resource documentation"
        }
    return jsonify({
        "status":404,
        "message":"message"
    })

@bluep.app_errorhandler(500)
def sys_error_found(error):
    
    return jsonify({
        "status":404,
        "message":"message"
    })