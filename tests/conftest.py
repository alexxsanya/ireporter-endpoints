import pytest 
from flask import Flask, jsonify, Blueprint

@pytest.fixture
def app():
    app = Flask(__name__) 
    bluep = Blueprint("bluep", __name__)
    app.register_blueprint(bluep, url_prefix="/api/v1")
    return app