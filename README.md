# testSurvey
Demo flask app for experiments

log:

Doc for testSurvey

Download and install PostgreSQL 
The installer PostgreSQL will ask you to set a password. 
Remember the password. It will be useful.  
Download and install pgAdmin4.


Enter virtual environment
```
pipenv install flask
pipenv install psycopg2 or pipenv run pip install psycopg2
pipenv install psycopg2-binary or pipenv run pip install psycopg2-binary
pipenv install flask-sqlalchemy
pipenv install gunicorn
```

select correct virtual env interpreter

write code 

click into pgAdmin 4

under databases, create a new database named testSurvey

go into testSurvey - schemas - tables, no tables at this point

when typing db.Column, error "SQLAlchemy doesn't have member .Column"

in vscode, select linter, switched from pylint to flake8. error resolved. 

Need to create feedback table (currently we're in dev, database will be local)

Go into python script in terminal

type:
```
from app import db
db.create_all() # creates feedback table
```
then exit

run server again

On pgadmin4, there should be a feedback table under Tables 

go into flask web app, put in an id and drag slider

click submit

Go back to pgadmin4 and refresh

right click on feedback - view/edit data - all rows

now you can see data

if you put in the same ID, the slider value won't be added to the database

if no id is entered into user ID field, the app will ask to enter ID


###### use below to deploy to heroku after changing code ######


To deploy: 

istall heroku cli by downloading istaller from https://devcenter.heroku.com/articles/heroku-cli. 

Or with mac:
```
brew tap heroku/brew && brew install heroku
```
make .gitignore file in vscode

in vscode terminal, type:
```
git init
heroku login
heroku create testexpt    # only lowercase letters are allowed
# add hobby-dev database on heroku:
heroku addons:create heroku-postgresql:hobby-dev --app testexpt
# gettinng the url of database
heroku config --app testexpt
```

now we need to upload files to heroku and let heroku know how to run app
```
# go to heroku dev center for help if needed
# create requirements 
pip freeze > requirements.txt
touch Procfile
touch runtime.txt (specify python version in this file)
git add . && git commit -m 'Initial Deploy'
# push to heroku
heroku git:remote -a testexpt
git push heroku master
# create table
heroku run python
> from app import db
> db.create_all()
> exit()
# access database:
heroku pg:psql --app testexpt
select * from feedback;  # press control z to quit connection from database
heroku open # opens app
```

###### export data from heroku postgresql ######
```
heroku pg:backups:capture
heroku pg:backups:download (this is download a dump file)
# restore dump into local database:
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U myuser -d mydb latest.dump 
```
You need to change myuser to your actual user on pgAdmi (can be found on server interface).

You need to change mydb to the name of your database. 

In my case, myuser = postgres, mydb = testSurvey

NOTE: If there are multiple dumps, latest.dump needs to be changed to the correct name

open pgAdmin4, look at testSurvey - Schemas - tables - feedback 

in upper right corner, click download

data will be downloaded as a csv file. 

NOTE: We can use some sort of api and build another app that presents data to researchers.



