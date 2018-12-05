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
    
    def test_
    #def test_create_this_red_flag(self, client): 
        #pass