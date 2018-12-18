class Validator:
    def __init__(self):
        pass
    def validate_incident(self, incidentObject):
        if "idd" in incidentObject and "ttype" in incidentObject and "status" in incidentObject:
            return True 

    def validate_user(self, userObject):
        if "firstname" in userObject and "email" in userObject and "registered" in userObject:
            return True 