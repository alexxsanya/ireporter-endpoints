from flask import Flask
from view import bluep

app = Flask(__name__) 

app.register_blueprint(bluep, url_prefix="/api/v1")