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


# Create an APISpec
template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Restful Swagger",
        "description": "Anastasia Lavrova, BMSTU",
        "version": "0.1.1",
        "contact": {
            "name": "Anastasia Lavrova",
            "url": "https://github.com/anastasialavrova",
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]

}

app.config['SWAGGER'] = {
    "swagger": "2.0",
    'title': 'My API',
    'uiversion': 3,
    "specs_route": "/",
    "route": '/apispec_1.json'
}
swagger = Swagger(app, template=template)
app.config.from_object(config.Config)
api = Api(app, version='2.0', title='Sample API',
    description='A sample API')
