from flask import jsonify, make_response, abort
statuses = ("draft", "resolved", "rejected","under investigation")
incident_types = ("red-flag", "investigation")

class IncidentValidator:
    def __init__(self):
        pass
    def validate_incident(self, incidentObject): 
        if 'idd' not in incidentObject or incidentObject['idd'] == '' or incidentObject['idd'] is int:
            abort(make_response(jsonify({
                "status": 400,
                "message": "The created incident must have an valid id with it"
            }), 400))
            
        if 'ttype' not in incidentObject or incidentObject['ttype'] == '' or incidentObject['ttype'] is int or incidentObject['ttype'] not in incident_types:
            abort(make_response(jsonify({
                "status": 400,
                "message": "Incident_type must be either a red-flag or Intervention record"
            }), 400))

        if 'location' not in incidentObject or incidentObject['location'] == '' or type(incidentObject['location']) is not str:
            abort(make_response(jsonify({
                "status": 400,
                "message": "location must be filled and must be a string in the form 'lat,long' "
            }), 400))

        if 'status' not in incidentObject or incidentObject['status'] not in statuses:
            abort(make_response(jsonify({
                "status": 400,
                "message": "status must be either (draft, resolved, rejected,under investigation)"
            }), 400))

        if type(incidentObject['comment']) is int:
            abort(make_response(jsonify({
                "message": "Comment must be a sentence",
                "status": 400
            }), 400))
        return True