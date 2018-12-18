class Validator:
    def validate_incident(incidentObject):
        if "idd" in incidentObject and "ttype" in incidentObject and "status" in incidentObject:
            return True 

    def validate_user(userObject):
        if "firstname" in userObject and "email" in userObject and "registered" in userObject:
            return True 