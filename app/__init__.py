from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "Secret Key"

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql:3306/assetManagement'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{usr}:{passwd}@mysql:3306/{db}'.format(
    usr=os.getenv('MYSQL_USER'), passwd=os.getenv('MYSQL_PASS'), db=os.getenv('MYSQL_DB'))


app.config['SQALALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

from app import routes