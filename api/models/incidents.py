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
                    },
                    {
                        "idd" : 2,
                        "title" : "Corrupt RDC in Gulu Ditrict",
                        "ttype" : "red-flag",
                        "comment" : "He is conienving with the chinese to steal resident's land" ,
                        "location" : "0.364242, 32.35338",
                        "images" : ["d:\img1.jpg","d:\img3.jpg","d:\img3.jpg"],
                        "status" : "rejected",
                        "createdOn" : str(datetime.datetime.now())[:10],
                        "createdBy" : 4
                    },
                    {
                        "idd" : 3,
                        "title" : "Police man asking for a bribe",
                        "ttype" : "red-flag",
                        "comment" : "Police man asking for a bribe just to see my friend who is an inmate",
                        "location" : "0.374242, 32.85338",
                        "images" : ["d:\img1.jpg","d:\img3.jpg","d:\img3.jpg"],
                        "status" : "under investigation",
                        "createdOn" : str(datetime.datetime.now())[:10],
                        "createdBy" : 4
                    }
                ]
