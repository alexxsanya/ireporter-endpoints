from flask import Blueprint

bluep = Blueprint("api",__name__,url_prefix='/api/v1')

@bluep.route('/red-flags', method="GET")
def get_all_red_flags():
    pass

@bluep.route('/red-flags/<int:red_flag_id>', method = "GET")
def get_this_red_flag(red_flag_id):
    pass

@bluep.route('/red-flags', method = "POST")
def create_this_red_flag():
    pass

@bluep.route('/red-flags/<int:red_flag_id>/location', method = "PATCH")
def update_red_flag_location(red_flag_id,location):
    pass

@bluep.route('/red-flags/<int:red_flag_id>/comment', method = "PATCH")
def update_red_flag_comment(red_flag_id, comment):
    pass

@bluep.route('/red-flags/<int:red_flag_id>', method = "DELETE")
def delete_red_flag(red_flag_id):
    pass
