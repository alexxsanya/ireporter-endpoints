from os import environ
def config():
    try: 
        db = {}
        db['host'] = environ.get("HOST")
        db['user'] = environ.get("USER")
        db['password'] = environ.get("PASSWORD")
        db['database'] = environ.get("DBNAME")
        return db
    except Exception:
        raise Exception