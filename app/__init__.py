from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql:3306/assetManagement'

app.config['SQALALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

from app import routes