import unittest
import requests  
from flask import jsonify , Flask
import pytest 


# tests/test_login.py 
import pytest
import json 
import api

@pytest.mark.usefixtures('client_class')
class TestLogin:  
    def test_apis_return_200_with_valid_parameter(self,test_client):
        assert app.test_client().get("http://google.com").status_code == 200, "This resource should exists" 
        assert app.test_client().get("/api/v1/redflags/1").status_code == 200, "This resource should exist"
        
    def test_apis_return_404_when_with_invalid_parameter(self,test_client):
        assert self.test_client.get("/api/v1/redflagsvc").status_code == 404, "This resource doesn't exits" 
        assert self.test_client.get("/api/v1/redflags/1").status_code == 404, "This resource doesn't exist"

    #def test_create_this_red_flag(self, client): 
        #pass
        