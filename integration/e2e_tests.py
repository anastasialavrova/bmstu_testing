import unittest
import requests
import os
# from mock import patch


from env import app
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

        def test_get_news(self):
            expected_result = {"message": "List of news"}
            r = requests.get('http://127.0.0.1:5000/news')
            assert r.status_code == 200
            assert expected_result == r.json()

        def test_post_news(self):
            expected_result = {"text": "text", "title": "title"}
            r = requests.post('http://127.0.0.1:5000/news?news_title=title&news_text=text')
            assert r.status_code == 200
            assert expected_result == r.json()

        def test_get_doctors(self):
            expected_result = {'message': 'List of doctors'}
            r = requests.get('http://127.0.0.1:5000/doctors')
            assert r.status_code == 200
            assert expected_result == r.json()

        def test_post_records(self):
            expected_result = {"diagnosis": "hello", "login_patient": "1"}
            r = requests.post('http://127.0.0.1:5000/records?rec_login=1&rec_diag=hello')
            assert r.status_code == 200
            assert expected_result == r.json()


        '''@patch('api.AddDiagnosis.find_in_db', return_value=1)
        def test_find_None_record(self, find_in_db):
            diagnosis = AddDiagnosis()
            rec = diagnosis.find_record('login2', find_in_db)
            assert rec == True

        @patch('api.Users.find_in_db', return_value=UserBuild().build())
        def test_sign_in_user(self, find_in_db):
                user = Users('login1', 'password1')
                assert user.sign_up(find_in_db) == 'user_space'
                '''

        def test_get_news(self):
            expected_result = "Ok"
            r = requests.get('http://127.0.0.1:5000/records/id')

            assert r.status_code == 200
            assert expected_result == r.json()


if __name__ == '__main__':
    os.system("python3 api.py")
    unittest.main()