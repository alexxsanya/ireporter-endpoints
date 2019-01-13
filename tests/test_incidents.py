import pytest
import json 

incident = {
	"idd":"45",
    "title": "Police man asking for a bribe",
    "ttype": "red-flag",
    "comment": "Police man asking for a bribe just to see my friend who is an inmate",
    "location": "0.3742423285338",
    "images": [
        "d:\\img1.jpg",
        "d:\\img3.jpg",
        "d:\\img3.jpg"
    ],
    "status": "under investigation",
    "createdOn": "13-Nov-2018",
    "createdBy": 4
}  
class TestIncidentsAPI: 
    def test_create_incident(self,client):
        response = client.post('/api/v1/redflags', json=incident, content_type='application/json')   
        result = json.loads(response.data)  
        assert "Incident has been created" == result['message']
        assert response.status_code == 201, "Incident is created"
        
    def test_create_incident_without_id_failing(self,client):
        incident = {   #without id
            "title": "Police man asking for a bribe ", 
            "comment": "Police man asking for a bribe just to see my friend who is an inmate",
            "location": "0.374242,3285338",
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
                                json=incident,
                                content_type='application/json')  
        result = json.loads(response.data)     
        assert "The created incident must have an valid id with it" == result['message'] 
        assert response.status_code == 400
    
    def test_create_incident_without_location_failing(self,client):
        incident = {    
            "idd":"57",
            "title": "Police man asking for a bribe",
            "ttype": "red-flag", 
            "comment": "Police man asking for a bribe just to see my friend who is an inmate", 
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
                                json=incident,
                                content_type='application/json')  

        result = json.loads(response.data)     
        assert "location must be filled and must be a string in the form 'lat,long' " == result['message'] 
        assert response.status_code == 400  

    def test_create_incident_without_status_failing(self,client):
        incident = { 
            "idd":"87",
            "title": "Police man asking for a bribe",
            "ttype": "red-flag",
            "comment": "Police man asking for a bribe just to see my friend who is an inmate",
            "location": "0.3742423285338",
            "images": [
                "d:\\img1.jpg",
                "d:\\img3.jpg",
                "d:\\img3.jpg"
            ], 
            "status":"fhf",
            "createdOn": "13-Nov-2018",
            "createdBy": 4
        }       
        response = client.post('/api/v1/redflags',
                                json=incident,
                                content_type='application/json')      
        result = json.loads(response.data)     
        assert "status must be either (draft, resolved, rejected,under investigation)" == result['message'] 
        assert response.status_code == 400   

    def test_create_incident_invalid_comment_failing(self,client):
        incident = { 
            "idd":"67",
            "title": "Police man asking for a bribe",
            "ttype": "red-flag",
            "comment": 6785768576,
            "location": "0.3742423285338",
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
                                json=incident,
                                content_type='application/json')   
        result = json.loads(response.data)     
        assert "Comment must be a sentence" == result['message'] 
        assert response.status_code == 400  

    def test_doc_page(self, client): 
        response = client.get('api/v1/')
        assert response.status_code == 200

    def test_incorrect_incident_type_input(self, client): 
        incident = {
            "idd":"95",
            "title": "Police man asking for a bribe",
            "ttype": "flagged",
            "comment": "Police man asking for a bribe just to see my friend who is an inmate",
            "location": "0.374242,3285338",
            "images": [
                "d:\\img1.jpg",
                "d:\\img3.jpg",
                "d:\\img3.jpg"
            ],
            "status": "rejected",
            "createdOn": "13-Nov-2018",
            "createdBy": 4
        } 
        response = client.post('/api/v1/redflags', json=incident, content_type='application/json')   
        result = json.loads(response.data)   
        assert "Incident_type must be either a red-flag or Intervention record" == result['message'] 
        assert response.status_code == 400  

    def test_all_incidents_returned(self, client):
        response = client.get('api/v1/redflags') 
        data = json.loads(response.data) 
        assert response.status_code == 200 
    
    def test_single_incident_returned(self, client):
        response = client.get('api/v1/redflags/1') 
        assert response.status_code == 200     

    def test_no_incident_is_with_wrong_id(self, client):
        response = client.get('api/v1/redflags/432823')
        data = json.loads(response.data)  
        assert data['status'] == 200 
        assert data['message'] == "No data found for the provided ID"
    
    def test_update_comment_success(self,client):
        comment = {
                    "comment":"The above incident is so urgent, please work on it"
                }
        response = client.patch("/api/v1/redflags/1/comment",content_type='application/json',json=comment)
        data = json.loads(response.data) 
        assert data['comment'] == "The comment has been updated successfully"
        assert data['status'] == 200

    def test_update_comment_failure(self,client):
        comment = {"comment":"The above incident is so urgent, please work on it" }
        response = client.patch("/api/v1/redflags/4734/comment",content_type='application/json',json=comment)
        data = json.loads(response.data) 
        assert data['comment'] == "Comment has not been modified"
        assert data['status'] == 200     

    def test_update_location_failure(self,client):
        location = {"location":"0.23242,32.132343" }
        response = client.patch("/api/v1/redflags/4734/location",content_type='application/json',json=location)
        data = json.loads(response.data) 
        assert data['error'] == "Location not modified"
        assert data['status'] == 204    

    def test_update_location_success(self,client):
        location = {"location":"0.23242,32.132343" }
        response = client.patch("/api/v1/redflags/1/location",content_type='application/json',json=location)
        data = json.loads(response.data) 
        assert data['comment'] == "Location has been successfully update"
        assert data['status'] == 200 

    def test_deleting_incident_success(self,client): 
        red_flag_id = 1
        response = client.delete("/api/v1/redflags/"+str(red_flag_id))
        data = json.loads(response.data)  
        assert "The record has been deleted successfully" == data['message']
        assert red_flag_id == data['id']
        assert data['status'] == 200 

    def test_deleting_incident_failure(self,client): 
        red_flag_id = 273267
        response = client.delete("/api/v1/redflags/"+str(red_flag_id))
        data = json.loads(response.data)  
        assert "No record found with the provided id" == data['message']
        assert red_flag_id == data['id']
        assert data['status'] == 204
