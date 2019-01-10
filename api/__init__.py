from flask import Flask, render_template
from api.views.__init__ import bluep
from flask_jwt_extended import JWTManager
app = Flask(__name__) 

SECRET_KEY = os.getenv('SECRETE_KEY', "precious")
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=360)
jwt = JWTManager(app)

@app.route('/')
@app.route('/api')
@app.route('/api/')
@app.route('/api/v1')
@app.route('/api/v1/')
def usage_guide():
    return render_template("usage.html") 


app.register_blueprint(bluep, url_prefix="/api/v1")