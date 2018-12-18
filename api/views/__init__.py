from flask import Blueprint,jsonify, request, Response
import datetime,json
from api.models.incidents import Incidents
from api.models.users import Users
from api.utility.validate import Validator
bluep = Blueprint("bluep", __name__)
incidents = Incidents.incidentsdb
users  = Users.userdb 
validator = Validator()

@bluep.route('/user', methods = ['POST'])
def create_user(): 
    user_data_object = request.get_json()
    if (validator.validate_user(user_data_object)):
        users.append({ 
            "id": 4,
            "firstname" : user_data_object['firstname'],
            "lastname" : user_data_object['lastname'],
            "othername" : user_data_object['othername'],
            "email" : user_data_object['email'],
            "username" : user_data_object['username'],
            "phoneNumber" : user_data_object['phoneNumber'],
            "registered" : str(datetime.datetime.now()),
            "isAdmin" : user_data_object['isAdmin'],
        })
        return Response(json.dumps({
            "status" : 201,
            "comment": b"User - "+ str({user_data_object['username']}) +"has been created"
        }), 201, mimetype="application/json")  
    else:
        return Response(json.dumps({
            "error": "Invalid Incident object",
            "help_string":
                "Request format should be {'username': 'jonh2',"
                "'fistname': 'John','lastname': 'Doe' ... }"
        }), status=400, mimetype="appliation/json") 

@bluep.route('/redflags', methods=['GET'])
def get_all_red_flags():
    return jsonify({'status':200,'data': incidents})

@bluep.route('/redflags/<int:red_flag_id>', methods = ['GET'])
def get_this_red_flag(red_flag_id):  
    return jsonify({'status':200,'data': [item for item in incidents if item['idd'] == red_flag_id]})  

@bluep.route('/redflags', methods = ['POST'])
def create_this_red_flag(): 
    redflag_data = request.get_json()
    if (validator.validate_incident(redflag_data)):

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
        return Response("Incident has been created", 201, mimetype="application/json") 
    else:
        return Response(json.dumps({
            "error": "Invalid Incident object",
            "help_string":
                "Request format should be {'title': 'corrupt president',"
                "'ttype': 'red-flag','status': 'pending' }"
        }), status=400, mimetype="appliation/json") 

@bluep.route('/redflags/<int:red_flag_id>/location', methods = ['PATCH'])
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
        return jsonify({'status':200,'comment': "update successful"})
    else:
        return jsonify({'status':405,'comment': "Not Updated",'Tip':"provided incident id could be wrong"})

@bluep.route('/redflags/<int:red_flag_id>/comment', methods = ['PATCH'])
def update_red_flag_comment(red_flag_id):
    request_data = request.get_json()
    
    updated_incident = {}
    updated = False

    if ("comment" in request_data):

        updated_incident["comment"] = request_data["comment"] 

        for red_flag in incidents:

            if red_flag["idd"] == red_flag_id:

                red_flag.update(updated_incident) 
                updated = True
    if updated:
        return jsonify({'status':200,'comment': "update successful"})
    else:
        return jsonify({'status':405,'comment': "Not Updated",'Tip':"provided incident id could be wrong"})

@bluep.route('/redflags/<int:red_flag_id>', methods = ['DELETE'])
def delete_red_flag(red_flag_id):
    try:
        flag_to_delete = [flag for flag in incidents if flag['idd'] == red_flag_id]
        if flag_to_delete is not None:
            incidents.remove(flag_to_delete[0])
            return jsonify({'status':200,'data': [{'id':red_flag_id,'message':"red flag record has been deleted"}]}) 
    except IndexError:     
        return jsonify({'status':400,'data': [{'id':red_flag_id,'message':'wrong record id was provided'}]}) 