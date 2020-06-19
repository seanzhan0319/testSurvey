from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from pytrics_get import pytrics_get, pytrics_data

app = Flask(__name__, static_url_path = "/", static_folder = "")

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


# model
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    # String(limit of char)
    userID = db.Column(db.String(20), unique=True)
    sliderVal = db.Column(db.Integer)

    def __init__(self, userID, sliderVal):
        self.userID = userID
        self.sliderVal = sliderVal


class DataJoin(db.Model):
    __tablename__ = 'datajoin'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(20), unique=True)
    q3_response = db.Column(db.Integer)

    def __init__(self, userID, q3_response):
        self.userID = userID
        self.q3_response = q3_response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        userID = request.form['userid']
        # need to store slider value
        sliderVal = request.form['myRange']
        if userID == '':
            return render_template('index.html',
                                   message='Please enter User ID')
        # if customer does't exist
        if db.session.query(Feedback).filter(Feedback.userID == userID).\
                count() == 0:
            data = Feedback(userID, sliderVal)
            db.session.add(data)
            db.session.commit()
            return render_template('thankyou.html')
        return render_template('index.html',
                               message='You have already submitted')


@app.route('/pytrics_retrieve', methods=['POST'])
def pytrics_retrieve():
    return pytrics_get()


@app.route('/pytrics_return')
def pytrics_return():
    try:
        return send_file('SV_eQl4Bl9zA0b9rHD_responses.zip', attachment_filename='data.zip')
    except Exception as e:
        return str(e)

@app.route('/pytrics_json_data', methods=['POST'])
def pytrics_json_data():
    try:
        return pytrics_data()
    except Exception as e:
        return str(e)

""" @app.route('/pytrics_flask_data_join', methods=['POST'])
def pytrics_flask_data_join():
    try:
        json_set = pytrics_data() """


if __name__ == '__main__':
    app.run()
