import pytest
import json  
 
data = { 
        "firstname" : "Alex",
        "lastname" : "Ssanua",
        "othername" : "Denis",
        "email" : "alexxssnvy@gmail.com",
        "username" : "alexsa",
        "password":"uganda123",
        "phonenumber" : "256788155220",
        "registered" : "2018-12-05",
        "isAdmin" : "false"
    }
cred =  {
            "username" : "alexxa",
            "password": "uganda",
        } 
class TestUserAPI:
    def test_application_exists(self, client):
        response = client.get('/api/v1/')
        assert response.status_code == 200
        assert b"guidance on how to use this API" in response.data
        
    def test_create_user(self,client):
        response = client.post('/api/v1/user',
                                json=data,
                                content_type='application/json')   
        assert response.status_code == 201, "Incident is created"  

    def test_password_should_be_atleast_8_characters_on_create_user(self,client): 
        data = { 
                "firstname" : "Alex",
                "lastname" : "Ssayfua",
                "othername" : "Denis",
                "email" : "denis@gmal.you", 
                "username" : "newusers1",
                "password":"ab12",#with less than the acceptable characters
                "phonenumber" : "256788155220",
                "registered" : "2018-12-05",
                "isAdmin" : "false"
            }
        response = client.post('/api/v1/user',json=data, content_type="application/json")
        result = json.loads(response.data)  
        assert result['error'] == "Password is required & must be atleast 8 characters"
        assert response.status_code == 400  

    def test_create_user_with_existant_username_fails(self, client):
        data = { 
                "firstname" : "Paul",
                "lastname" : "Muwanga",
                "othername" : "Steven",
                "email" : "stevepaul@gmal.you", #with less than the acceptable characters
                "username" : "alexxa",
                "password":"ab125fgfdgg",
                "phonenumber" : "256788155228",
                "registered" : "2018-12-05",
                "isAdmin" : "false"
            }
        response = client.post('/api/v1/user',json=data, content_type="application/json")
        result = json.loads(response.data)  
        assert result['error'] == "User name already exists"
        assert response.status_code == 400     

    def test_create_user_with_existant_phonenumber_fails(self, client):
        data = { 
                "firstname" : "Eve",
                "lastname" : "Nuwa",
                "othername" : "St",
                "email" : "alexxsanya@gmail.com", 
                "username" : "eve5656",
                "password":"ab125fgfdgg",
                "phonenumber" : "256788155229",
                "registered" : "2018-12-05",
                "isAdmin" : "false"
            }
        response = client.post('/api/v1/user',json=data, content_type="application/json")
        result = json.loads(response.data)  
        assert result['error'] == "The Supplied Email Address already exists"
        assert response.status_code == 400  

    def test_create_user_with_incorrect_email_format(self,client):
        data = { 
                "firstname" : "Joel",
                "lastname" : "Jame",
                "othername" : "Stv",
                "email" : "alexxsanya@.com", #incorrect email address
                "username" : "joels34",
                "password":"ab125fgfdgg",
                "phonenumber" : "256788155239",
                "registered" : "2018-12-05",
                "isAdmin" : "false"
            }
        response = client.post('/api/v1/user',json=data, content_type="application/json")
        result = json.loads(response.data) 
        assert result['error'] == "email must be of the form (user@domain.xxx)"
        assert response.status_code == 400  
                
    def test_incorrect_firstname_input(self,client):
        data["firstname"]= 237264 
        response = client.post('/api/v1/user',
                                json=data,
                                content_type='application/json')   
        assert response.status_code == 400

    def test_incorrect_lastname_input(self,client):
        data["lastname"]= 237264 
        response = client.post('/api/v1/user',
                                json=data,
                                content_type='application/json')   
        assert response.status_code == 400

    def test_incorrect_othername_input(self,client):
        data["othername"]= 237264 
        response = client.post('/api/v1/user',
                                json=data,
                                content_type='application/json')   
        assert response.status_code == 400

    def test_incorrect_username_input(self,client):
        data["username"]= 4 
        response = client.post('/api/v1/user',
                                json=data,
                                content_type='application/json')   
        assert response.status_code == 400

    def test_incorrect_emailaddress_input(self,client):
        data["email"]= "incorrectemail@gmail" 
        response = client.post('/api/v1/user',
                                json=data,
                                content_type='application/json')   
        assert response.status_code == 400

    def test_incorrect_phonenumber_input(self,client):
        data = { 
                "firstname" : "Jame",
                "lastname" : "Kenya",
                "othername" : "Pa",
                "email" : "kenyerr@gmail.com",
                "username" : "kenyarr",
                "password":"uganda123",
                "phonenumber" : "082473278233", #it should be like (256 *** *** ***)
                "registered" : "2018-12-05",
                "isAdmin" : "false"
            } 
        response = client.post('/api/v1/user',
                                json=data,
                                content_type='application/json')   
        result = json.loads(response.data)  
        assert result['error'] == "Enter valid phone number eg (256 *** *** ***) like (256788111222)" 
        assert response.status_code == 400

    def test_incorrectlength_phonenumber_input(self,client):
        data = { 
                "firstname" : "Allex",
                "lastname" : "Ssanjua",
                "othername" : "Dennis",
                "email" : "incorrectlenght@gmail.com",
                "username" : "ssanjdenee",
                "password":"uganda123",
                "phonenumber" : "2567881552256560",
                "registered" : "2018-12-05",
                "isAdmin" : "false"
            }
        response = client.post('/api/v1/user', json=data, content_type='application/json') 
        result = json.loads(response.data)  
        assert result['error'] == "Phone number should have 12 digits"  
        assert response.status_code == 400

    def test_incorrect_phonenumber_with_characters(self,client):
        data = { 
                "firstname" : "Alex",
                "lastname" : "Ssanua",
                "othername" : "Denis",
                "email" : "stevenpp@gmail.com",
                "username" : "alexsa",
                "password":"uganda123",
                "phonenumber" : "13134sdfsf",
                "registered" : "2018-12-05",
                "isAdmin" : "false"
            } 
        response = client.post('/api/v1/user',json=data, content_type='application/json')   
        result = json.loads(response.data)   
        assert result['error'] == "Phone number should only contain digits" 
        assert response.status_code == 400  

    def test_login(self, client):
        cred =  {
                    "username" : "alexxa",
                    "password": "uganda256",
                }
        response = client.post('/api/v1/login', json=cred, content_type="application/json")
        assert response.status_code == 200

    def test_login_with_wrong_user_name(self, client):
        
        cred["username"] = "alexxsa"
        cred['password'] =""
        response = client.post('/api/v1/login', content_type="application/json", json=cred)
        result = json.loads(response.data)  
        assert result['error'] == "Password has not been supplied"

    def test_login_with_wrong_cred_meeting_standards(self, client):
        cred["password"] = "sg33dsjhkjad"
        cred["username"] = "alexxsa"
        response = client.post('/api/v1/login', content_type="application/json", json=cred)
        result = json.loads(response.data)  
        assert result['error'] == "Invalid username or password"
        assert response.status_code == 400
     