from flask import Blueprint

bluep = Blueprint("bluep", __name__)

@bluep.route('/redflags', methods=['GET'])
def get_all_red_flags():
    return "ffd"

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
