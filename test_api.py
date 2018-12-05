import pytest

@pytest.mark.usefixtures('client_class')
class TestLogin:  

    def test_apis_return_200_with_valid_parameter(self,client):
        assert 1 == 1
        #assert client.get("http://google.com").status_code == 200, "This resource should exists" 
        assert client.get("/api/v1/redflags/15").status_code == 200, "This resource should exist"
        
    def test_apis_return_404_when_with_invalid_parameter(self,client):
        assert client.get("/api/v1/redflagsvc").status_code == 404, "This resource doesn't exits" 
        assert client.get("/api/v1/redflags/fv").status_code == 404, "This resource doesn't exist"
    
    def test_if_get_api_with_invalid_par_return_404_not_found(self,client):
        assert b'404 Not Found' in client.get("/api/v1/redflags/1n64").data 

    '''def test_that_valid_JSON_is_passed_to_api(self,client):
        """Test status code 405 from improper JSON on post to raw"""
        response = client.post('/redflags',
                                data="This isn't a json... it's a string!",
                                content_type='application/json')
        assert response.status_code == 405, "This provided data should be a json object" '''

    def test__post_api_return_bad_request_400_with_wrong_requests(self,client):
        #testing for bad request when given invalid json parameters 400 Bad Request
        response = client.post('/api/v1/redflags',
                                data="This isn't a json... it's a string!",
                                content_type='application/json')
        assert response.status_code == 400, "the passed data should be of application\json"
        assert b'400 Bad Request' in response.data

    def test_create_this_red_flag_return_success_when_provided_with_valid_json(self,client):
        incident_data = {
            "idd": 4,
            "title": "Police man asking for a bribe",
            "ttype": "red-flag",
            "comment": "Police man asking for a bribe just to see my friend who is an inmate",
            "location": "0.374242, 32.85338",
            "images": [
                "d:\\img1.jpg",
                "d:\\img3.jpg",
                "d:\\img3.jpg"
            ],
            "status": "under investigation",
            "createdOn": "13-Nov-2018",
            "createdBy": 4
        }
        response = client.post('/api/v1/redflags',
                                json=incident_data,
                                content_type='application/json')  
        assert response.status_code == 201, "Incident is created"                                  
    