import unittest
import requests  
from flask import jsonify , Flask
import pytest 


# tests/test_login.py 
import pytest
import json
from flask import url_for 

import pytest
import json
from flask import url_for

@pytest.mark.usefixtures('client_class')
class TestLogin:
    def test_if_create_red_flag_apiv1_is_inexistent(self, client):
        assert client.get("/api/v1").status_code == 404, "This resource doesn't exits" 

    def test_create_this_red_flag(self, client): 
        pass
