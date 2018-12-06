# i-Reporter API

Corruption is a huge bane to Africa’s development. African countries must develop novel and localized solutions that will curb this menace, hence the birth of iReporter.  iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention.

Therefore this the API to power the UI application located here [github](https://github.com/alexxsanya/iReporter)

### Build Status

[![Build Status](https://travis-ci.org/alexxsanya/ireporter-endpoints.svg?branch=develop)](https://travis-ci.org/alexxsanya/ireporter-endpoints)  [![Coverage Status](https://coveralls.io/repos/github/alexxsanya/ireporter-endpoints/badge.svg?branch=develop)](https://coveralls.io/github/alexxsanya/ireporter-endpoints?branch=develop)  [![Maintainability](https://api.codeclimate.com/v1/badges/046278bc19fd77812d41/maintainability)](https://codeclimate.com/github/alexxsanya/ireporter-endpoints/maintainability)  [![Test Coverage](https://api.codeclimate.com/v1/badges/046278bc19fd77812d41/test_coverage)](https://codeclimate.com/github/alexxsanya/ireporter-endpoints/test_coverage)

### Features

1. Users can create a  red-flag record 
2. Users can edit their  red-flag records.
3. Users can delete their  red-flag records.
4. Users can add geolocation (Lat Long Coordinates) to their red-flag records.
5. Users can update the geolocation attached to their red-flag records. 



### API Usage

You may access the API via https://ireporter-ep.herokuapp.com

To access the various features of the API, the following are used.

##### API Versions

- Version 1 : https://ireporter-ep.herokuapp.com/api/v1

##### POST Methods

| END POINT | Request Format | Response Format | Description                  |
| --------- | -------------- | --------------- | ---------------------------- |
| /users    | 1.1            | 1.2             | To create a new user         |
| /redflags | 2.1            | 2.2             | To create a redflag incident |

##### GET Methods

| END POINT               | Response Format | Description                             |
| ----------------------- | --------------- | --------------------------------------- |
| /redflags               | 3.1             | Returns all created redflags            |
| /redflags/<red-flag-id> | 3.2             | Returns details of supplied red-flag-id |

##### PATCH  Methods

| END POINT                        | Request Format | Response Format | Description                                     |
| -------------------------------- | -------------- | --------------- | ----------------------------------------------- |
| /redflags/<red-flag-id>/location | 4.1            | 4.2             | Edit the location of a specific red-flag record |
| /redflags/<red-flag-id>/comment  | 5.1            | 5.2             | Edit the comment of a specific red-flag record  |

##### DELETE Method

| END POINT                | Response Format | Description                        |
| ------------------------ | --------------- | ---------------------------------- |
| /red-flags/<red-flag-id> | 6.1             | Delete a specific red flag record. |

### JSON objects Formats

1.1 JSON Request data for Creating a new user

```python
{
    "id" : Integer,
    "firstname" : String,
    "lastname" : String,
    "othernames" : String,
    "email" : String,
    "phoneNumber" : String,
    "username" : String,
    "registered" : Date,
    "isAdmin" : Boolean,
    "password": String, 
}
```
1.2 JSON Response after creating a new a user

```python
{
    "status": 201,
    "data": [{
        "id": Integer,
        "message": "New User Added!"}]
}
```
2.1 JSON Request data for posting a Incident

```python
{
    "id" : Integer,
    "createdOn" : Date,
    "createdBy" : Integer, # represents the user who created this record
    "type" : String, # [red-flag, intervention]
    "location" : String, # Lat Long coordinates
    "status" : String , # [draft, under investigation, resolved, rejected]
    "Images" : [Image, Image], 
    "title": String, 
    "comment" : String,
    "remarks" : String # Remarks are set by admin upon resolving an incident
}
```
2.2 JSON Response after posting an incident

```python
{
    "status" : Integer,
    "data" : [ {
        "id" : Integer, # red flag record primary key
        "message" : "Created red-flag record" } ]
}
```

3.1 JSON Response for return of all Red flag Incidents

```python
{
    "status":integer,
    "data":{[...],[...],[...]}
}
```

3.2 JSON Response object for a single returned red flag incident

```python
{
    "status":integer,
    "data":{[...]}
}
```

4.1 JSON Request data for updating Incident Location

```python
{   
 	"location": String # in formatted as ->  "Lat, Long" 
}
```

4.2 JSON Response data after updating Incident Location

```python
{   
    "status" : Integer,
 	"data": [{"id":Integer, #red-flag record primary key
              "message": "Updated red-flag record’s location"  }] 
}
```

5.1 JSON Request data for updating Incident comment

```python
{   
 	"comment": String 
}
```

5.2 JSON Response data after updating Incident comment

```python
{   
    "status" : Integer,
 	"data": [{"id":Integer, #red-flag record primary key
              "message": "Updated red-flag record’s comment" }] 
}
```

6.1 JSON Response data after deleting an incident

```python
{   
    "status" : Integer,
 	"data" : [{ "id":Integer,  // red-flag record primary key
                "message":"red-flag record has been deleted"}]  
}
```

