from flask import Flask, jsonify, render_template, request, send_file, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__, static_url_path = "/", static_folder = "")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['CORS_HEADERS'] = 'Content-Type'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    # dev database
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://postgres:123456@localhost/testSurvey'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgres://onijnjombokzhh:b71661552e670fb920ae4126dc7f798a3925675cb8'\
        'fed5dd73a06df9e06d56d1@ec2-34-202-88-122.compute-1.amazonaws.com:543'\
        '2/d5vubft84tih4p'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# creating database object
db = SQLAlchemy(app)

class SurveyEntry(db.Model):
    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(4294000000))
    value = db.column(db.String(4294000000))

    def __init__(self, name, value):
        self.name = name
        self.value = value

@app.route('/api/v1/GETtest')
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def GETTest():
    return jsonify(str("Success!"))

@app.route('/api/v1/dataPost', methods=['POST'])
@cross_origin()
def api_all():
    if request.method=='POST':
        posted_data = request.get_json()
        jsonData = posted_data['data']
        name = jsonData["name"]

        data = SurveyEntry(name, json.dumps(jsonData))
        db.session.add(data)
        db.session.commit()
        response = jsonify(str("Successfully stored  " + str(data)))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response