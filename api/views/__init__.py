from flask import Blueprint,jsonify, request, Response
import datetime,json

bluep = Blueprint("bluep", __name__)

@bluep.route('/redflags', methods=['GET'])
def get_all_red_flags():
    return jsonify({'status':200,'data': incidents})

@bluep.route('/redflags/<int:red_flag_id>', methods = ['GET'])
def get_this_red_flag(red_flag_id):
    incident = {}
    for item in incidents:
        if item['idd'] == red_flag_id:
            incident = item 
    return jsonify({'status':200,'data': incident})

@bluep.route('/redflags', methods = ['POST'])
def create_this_red_flag():
    request_data  = request.get_json() 
    if (valid_incident(request_data)):
        incident = { 
            "idd": 4,
            "title" : request_data['title'],
            "ttype" : request_data['ttype'],
            "comment" : request_data['comment'],
            "location" : request_data['location'],
            "images" : request_data['images'],
            "status" : request_data['status'],
            "createdOn" : str(datetime.datetime.now())[:10],
            "createdBy" : request_data['createdBy'],
        }
        incidents.append(incident)
        response = Response("", 201, mimetype="application/json") 
        return response
    else:
        bad_object = {
            "error": "Invalid Incident object",
            "help_string":
                "Request format should be {'title': 'corrupt president',"
                "'ttype': 'red-flag','status': 'pending' }"
        }
        response = Response(json.dumps(bad_object), status=400, mimetype="appliation/json")
        return response

@bluep.route('/redflags/<int:red_flag_id>/location', methods = ['PATCH'])
def update_red_flag_location(red_flag_id,location):
    request_data = request.get_json()
    
    updated_incident = {}
    updated = False

    if ("location" in request_data):

        updated_incident["location"] = request_data["location"] 

        for red_flag in incidents:

            if red_flag["idd"] == red_flag_id:

                red_flag.update(updated_incident) 
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
    for incident in incidents:
        if(incident['idd'] == red_flag_id):
            incidents.remove[incident]
            response = {'status':200,'data': [{'id':red_flag_id,'message':"red flag record has been deleted"}]}
            return jsonify( response )
        else:
            return jsonify({'status':400,'data': [{'id':red_flag_id,'message':'wrong record id was provided'}]}) 

def valid_incident(incidentObject):
    if "idd" in incidentObject and "ttype" in incidentObject and "status" in incidentObject:
        return True
    else:
        return False

incidents = [
    {
        "idd": 1,
        "title" : "Corrupt LC 3 in Mukono Ditrict",
        "ttype" : "red-flag",
        "comment" : "He is asking me for 5Million to get his approval",
        "location" : "0.324242, 32.55338",
        "images" : ["d:\img1.jpg","d:\img3.jpg","d:\img3.jpg"],
        "status" : "draft",
        "createdOn" : str(datetime.datetime.now())[:10],
        "createdBy" : 1
    },
    {
        "idd" : 2,
        "title" : "Corrupt RDC in Gulu Ditrict",
        "ttype" : "red-flag",
        "comment" : "He is conienving with the chinese to steal resident's land" ,
        "location" : "0.364242, 32.35338",
        "images" : ["d:\img1.jpg","d:\img3.jpg","d:\img3.jpg"],
        "status" : "rejected",
        "createdOn" : str(datetime.datetime.now())[:10],
        "createdBy" : 4
    },
    {
        "idd" : 3,
        "title" : "Police man asking for a bribe",
        "ttype" : "red-flag",
        "comment" : "Police man asking for a bribe just to see my friend who is an inmate",
        "location" : "0.374242, 32.85338",
        "images" : ["d:\img1.jpg","d:\img3.jpg","d:\img3.jpg"],
        "status" : "under investigation",
        "createdOn" : str(datetime.datetime.now())[:10],
        "createdBy" : 4
    }
]