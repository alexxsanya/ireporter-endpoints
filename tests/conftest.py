import pytest 
from flask import Flask, jsonify

@pytest.fixture
def app():
    app = Flask(__name__) 

    return app