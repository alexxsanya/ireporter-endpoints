from flask import Flask, render_template
from api.views.routes import bluep 
from flask_mail import Mail, Message
import os, datetime
app = Flask(__name__) 

@app.route('/api/v1/')
def usage_guide():
    return render_template("usage.html") 

app.register_blueprint(bluep, url_prefix="/api/v1")
mail=Mail(app)