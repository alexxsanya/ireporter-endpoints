from flask import Blueprint,jsonify, request, Response
import datetime,json
from api.models.incidents import Incidents
from api.models.users import Users
from api.utility.validate_incident import IncidentValidator
from api.utility.validate_user import UserValidator
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_jwt_extended import (create_access_token)
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
bluep = Blueprint("bluep", __name__)
incidents = Incidents.incidentsdb
users  = Users.userdb 
incidentValidator = IncidentValidator()
userValidator = UserValidator()

@bluep.route('/user', methods = ['POST'])
def create_user(): 
    user_data_object = request.get_json()
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

    for user in users:
        if user['username'] == user_data_object['username']:
                return jsonify({
                    "status": 400,
                    "error": "User name already exists"
                }), 400

    if not user_data_object['password']  or len(user_data_object['password']) < 8:
            return jsonify({
                "status": 400,
                "error": "Password is required & must be atleast 8 characters"
            }), 400

    users.append({ 
        "id": 4,
        "firstname" : user_data_object['firstname'],
        "lastname" : user_data_object['lastname'],
        "othername" : user_data_object['othername'],
        "email" : user_data_object['email'],
        "username" : user_data_object['username'],
        "password": generate_password_hash(user_data_object['password'], method='sha256'),
        "phonenumber" : user_data_object['phonenumber'],
        "registered" : str(datetime.datetime.now()),
        "isAdmin" : user_data_object['isAdmin'],
    })
    access_token = create_access_token(identity = user_data_object['username'])
    refresh_token = create_refresh_token(identity = user_data_object['username'])
    return Response(json.dumps({
        "status" : 201,
        "comment": "User - "+ str(user_data_object['username']) +"has been created",
        "access_token": access_token,
        'refresh_token': refresh_token
    }), 201, mimetype="application/json")  

@bluep.route('/login', methods = ['POST'])
def login_user():
    data = request.get_json()
    print(data)
    username = data['username']
    password = data['password']

    userValidator.validate_login(username, "username is required")
    userValidator.validate_login(password, "Password has not been supplied")
    for user in users: 
        print(check_password_hash(user['password'], password))
        print(user['username'] == username)
        if user['username'] == username and check_password_hash(user['password'], password):
            #access_token = create_access_token(username)
            access_token = create_access_token(identity = username)
            refresh_token = create_refresh_token(identity = username)
            print(user)
            return jsonify({
                "status": 200,
                "status": "Login successful",
                "access_token": access_token,
                'refresh_token': refresh_token
            }), 200

        return jsonify({"status": 400, "error": "Invalid username or password"}), 400

@bluep.route('/redflags', methods=['GET'])
@jwt_required
def get_all_red_flags(): 
        if len(incidents) <= 0:
            return jsonify({
                "Status": 400,
                "error": "No incident records in the database yet"
            }), 400
        else:
            return jsonify({'status':200,'data': incidents})

@bluep.route('/redflags/<int:red_flag_id>', methods = ['GET'])
@jwt_required
def get_this_red_flag(red_flag_id):   
    result = [item for item in incidents if item['idd'] == red_flag_id]
    if result != []:
        return jsonify({'status':200,'data': result}) 
    else:
        return jsonify({'status':400,'message':"No data found for the provided ID"})    

@bluep.route('/redflags', methods = ['POST'])
@jwt_required
def create_this_red_flag(): 
    redflag_data = request.get_json()
    if (incidentValidator.validate_incident(redflag_data)):

        incidents.append({ 
            "idd": 4,
            "title" : redflag_data['title'],
            "ttype" : redflag_data['ttype'],
            "comment" : redflag_data['comment'],
            "location" : redflag_data['location'],
            "images" : redflag_data['images'],
            "status" : redflag_data['status'],
            "createdOn" : str(datetime.datetime.now())[:10],
            "createdBy" : redflag_data['createdBy'],
        }) 
        return jsonify({
                "status": 201,
                "message": "Incident has been created", 
            }), 201

@bluep.route('/redflags/<int:red_flag_id>/location', methods = ['PATCH'])
@jwt_required
def update_red_flag_location(red_flag_id):
    location_data = request.get_json()
    
    updated_location = {}
    updated = False

    if ("location" in location_data):

        updated_location["location"] = location_data["location"] 

        for red_flag in incidents:

            if red_flag["idd"] == red_flag_id:

                red_flag.update(updated_location) 
                updated = True
    if updated:
        return jsonify({'status':200,'comment': "Location has been successfully update"})
    else:
        return jsonify({'status':200,'error': "Location not modified"})

@bluep.route('/redflags/<int:red_flag_id>/comment', methods = ['PATCH'])
@jwt_required
def update_red_flag_comment(red_flag_id):
    request_data = request.get_json()
    
    updated_incident = {}
    updated = False

    if ("comment" in request_data and len(request_data["comment"]) > 5 ):

        updated_incident["comment"] = request_data["comment"] 

        for red_flag in incidents:

            if red_flag["idd"] == red_flag_id:

                red_flag.update(updated_incident) 
                updated = True
    if updated:
        return jsonify({'status':200,'comment': "The comment has been updated successfully"})
    else:
        return jsonify({'status':200,'comment': "Comment has not been modified", 'tip':'cross-check the user id'})

@bluep.route('/redflags/<int:red_flag_id>', methods = ['DELETE'])
@jwt_required
def delete_red_flag(red_flag_id):
    try:
        flag_to_delete = [flag for flag in incidents if flag['idd'] == red_flag_id]
        if flag_to_delete is not None:
            incidents.remove(flag_to_delete[0])
            return jsonify({'status':200,'id':red_flag_id,'message':"The record has been deleted successfully"}) 
    except IndexError:     
        return jsonify({'status':200 ,'id':red_flag_id,'message':'No record found with the provided id'}) 