from flask import Flask
from views import bluep

app = Flask(__name__) 

@app.route('/')
@app.route('/api/v1')
@app.route('/api/v1/')
def usage_guide():
    return "Usage Guide"


app.register_blueprint(bluep, url_prefix="/api/v1")