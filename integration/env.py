from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from collections import namedtuple

app = Flask(__name__)
app.secret_key = 'i love bmstu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
manager = LoginManager(app)

Message = namedtuple('Message', 'text tag')
messages = []
SignUp = namedtuple('SignUp', 'login password')
log_and_pass = []

username = '0'

login_manager = LoginManager(app)


username = '0'



