from flask import Flask 
from api.views.__init__ import bluep

app = Flask(__name__) 

@app.route('/')
@app.route('/api')
@app.route('/api/')
@app.route('/api/v1')
@app.route('/api/v1/')
def usage_guide():
    return "<br /><h2 align='center'>Click <a href='https://github.com/alexxsanya/ireporter-endpoints/blob/develop/README.md'>Here</a> for guidance on how to use this API</h2>"


app.register_blueprint(bluep, url_prefix="/api/v1")