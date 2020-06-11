from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run()
