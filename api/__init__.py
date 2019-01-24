from flask import Flask, render_template
from api.views.routes import bluep 
from flask_mail import Mail, Message
import os, datetime
app = Flask(__name__) 

@app.route('/')
@app.route('/api')
@app.route('/api/')
@app.route('/api/v1')
@app.route('/api/v1/')
def usage_guide():
    return render_template("usage.html") 

app.register_blueprint(bluep, url_prefix="/api/v1")
mail=Mail(app)