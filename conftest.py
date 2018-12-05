import pytest
from flask import Flask, jsonify, Blueprint, request, Response, json
from api import app as ap

@pytest.fixture
def app():
    app = ap
    return app

