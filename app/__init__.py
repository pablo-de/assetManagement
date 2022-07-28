from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"

MYSQL_USER = 'user1'
MYSQL_PASS = '123456'
MYSQL_HOST = 'localhost'
MYSQL_DB = 'assetManagement'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{usr}:{passwd}@{host}/{db}'.format(
    usr=MYSQL_USER, passwd=MYSQL_PASS, host=MYSQL_HOST, db=MYSQL_DB)
app.config['SQALALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

from app import routes