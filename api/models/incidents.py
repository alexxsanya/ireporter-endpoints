import datetime,json

class Incidents:
    incidentsdb = [
                    {
                        "idd": 1,
                        "title" : "Corrupt LC 3 in Mukono Ditrict",
                        "ttype" : "red-flag",
                        "comment" : "He is asking me for 5Million to get his approval",
                        "location" : "0.324242, 32.55338",
                        "images" : ["d:\img1.jpg","d:\img3.jpg","d:\img3.jpg"],
                        "status" : "draft",
                        "createdOn" : str(datetime.datetime.now())[:10],
                        "createdBy" : 1
                    }
                ]
