import unittest
import requests
import os
# from mock import patch


from env import app, db
from api import AddDiagnosis, Users
from models import User, Doctors

from werkzeug.security import generate_password_hash

class UserBuild():
    def __init__(self):
        self.new_user = User(sign_login = 'login1', sign_password = generate_password_hash('password1'), sign_role = 1)

    def with_login(self, login):
        self.new_user.sign_login = login

    def with_password(self, password):
        self.new_user.sign_password = password

    def with_role(self, role):
        self.new_user.sign_role = role

    def build(self):
        return self.new_user

with app.app_context():
    class TestIntegrations(unittest.TestCase):
        def setUp(self):
            self.app = app.test_client()
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
            db.create_all()

        def test_e2e(self):
            r = requests.get('http://127.0.0.1:5000/')
            assert r.status_code == 200

            expected_result = {"message": "List of news"}
            r = requests.get('http://127.0.0.1:5000/news')
            assert r.status_code == 200
            assert expected_result == r.json()

            expected_result = {'message': 'List of doctors'}
            r = requests.get('http://127.0.0.1:5000/doctors')
            assert r.status_code == 200
            assert expected_result == r.json()

            # r = requests.get('http://127.0.0.1:5000/user_space')
            # assert r.status_code == 200

            r = requests.get('http://127.0.0.1:5000/user_space')
            assert r.status_code == 200

        def tearDown(self):
            db.session.remove()
            db.drop_all()



if __name__ == '__main__':
    os.system("python3 api.py")
    unittest.main()
