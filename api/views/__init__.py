from flask import Blueprint,jsonify, request, Response
import datetime

bluep = Blueprint("bluep", __name__)

@bluep.route('/redflags', methods=['GET'])
def get_all_red_flags():
     pass

@bluep.route('/redflags/<int:red_flag_id>', methods = ['GET'])
def get_this_red_flag(red_flag_id):
    pass

@bluep.route('/redflags', methods = ['POST'])
def create_this_red_flag():
    pass

@bluep.route('/redflags/<int:red_flag_id>/location', methods = ['PATCH'])
def update_red_flag_location(red_flag_id,location):
    pass

@bluep.route('/redflags/<int:red_flag_id>/comment', methods = ['PATCH'])
def update_red_flag_comment(red_flag_id, comment):
    pass

@bluep.route('/redflags/<int:red_flag_id>', methods = ['DELETE'])
def delete_red_flag(red_flag_id):
    pass

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