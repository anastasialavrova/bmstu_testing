import unittest
from mock import patch

from env import app, db

from models import User
from classes import Users

from models import Record
from classes import AddDiagnosis

from models import News
from classes import AddNews

from werkzeug.security import generate_password_hash

class UserBuild():
    def __init__(self):
        self.new_user = User(sign_login = 'login1', sign_password = 'password1', sign_role = 1)

    def with_login(self, login):
        self.new_user.sign_login = login

    def with_password(self, password):
        self.new_user.sign_password = password

    def with_role(self, role):
        self.new_user.sign_role = role

    def build(self):
        return self.new_user


class NewsBuild():
    def __init__(self):
        self.new_news = News(news_title = 'title1', news_text = 'text1')

    def with_login(self, title):
        self.new_news.news_title = title

    def with_password(self, text):
        self.new_news.news_text = text

    def build(self):
        return self.new_news


class RecordBuild():
    def __init__(self):
        self.record = Record(rec_login = 'login1', rec_diag = 'record1')

    def with_record(self, text):
        self.record.rec_diag = text

    def with_login(self, login):
        self.record.rec_login = login

    def build(self):
        return self.record

with app.app_context():
    class UserModelCase(unittest.TestCase):
        def setUp(self):
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
            db.create_all()

        def test_new_user(self):
            user = UserBuild().build()
            user.save_to_db()
            assert user.sign_login == 'login1'
            assert user.sign_password == 'password1'
            assert user.sign_role == 1

        @patch('classes.Users.check_hash', return_value=1)
        def test_sign_in_user(self, check_hash):
            with app.app_context():
                # записываем в БД эту запись
                user = User(sign_login='login1', sign_password='password1', sign_role=1)
                db.session.add(user)
                db.session.commit()

                # создаем экземпляр класса Users
                user = Users('login1', 'password1')
                assert user.sign_in(check_hash) == 'user_space'

        @patch('classes.Users.check_hash', return_value=1)
        def test_sign_in_doctor(self, check_hash):
            with app.app_context():
                # записываем в БД эту запись
                user = User(sign_login='login2', sign_password='password2', sign_role=2)
                db.session.add(user)
                db.session.commit()

                # создаем экземпляр класса Users
                user = Users('login2', 'password2')
                assert user.sign_in(check_hash) == 'doctor_space'

        @patch('classes.Users.check_hash', return_value=1)
        def test_sign_in_admin(self, check_hash):
            with app.app_context():
                # записываем в БД эту запись
                user = User(sign_login='login3', sign_password='password3', sign_role=3)
                db.session.add(user)
                db.session.commit()

                # создаем экземпляр класса Users
                user = Users('login3', 'password3')
                assert user.sign_in(check_hash) == 'admin_space'

        def test_user_login(self):
            with app.app_context():
                # записываем в БД эту запись
                hash_password = generate_password_hash('password1')
                user = User(sign_login=None, sign_password=hash_password, sign_role=3)
                assert user.save_to_db() == 'error'

        def test_user_password(self):
            with app.app_context():
                # записываем в БД эту запись
                user = User(sign_login='login1', sign_password=None, sign_role=3)
                # print(user.save_to_db())
                assert user.save_to_db() == 'error'

        def test_user_role(self):
            with app.app_context():
                # записываем в БД эту запись
                user = User(sign_login='login1', sign_password='password1', sign_role=None)
                # print(user.save_to_db())
                assert user.save_to_db() == 'error'

        def test_registration(self):
            with app.app_context():
                user = Users('login1', 'password1')
                assert user.registration('password1', 1) == 'ok'

        def test_registration_login(self):
            with app.app_context():
                user = Users(None, 'password1')
                assert user.registration('password1', 1) == 'Заполните все поля!'

        def test_registration_password(self):
            with app.app_context():
                user = Users('login1', 'password1')
                assert user.registration('password2', 1) == 'Пароли не совпадают'


        def tearDown(self):
            db.session.remove()
            db.drop_all()

    class NewsModelCase(unittest.TestCase):
        def setUp(self):
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
            db.create_all()

        def test_new_news(self):
            new_news = NewsBuild().build()
            new_news.save_to_db()
            assert new_news.news_title == 'title1'
            assert new_news.news_text == 'text1'

        def test_add_news(self):
            new_news = AddNews('title1', 'text1')
            assert new_news.add_news() == 'ok'

        def test_add_news_none_title(self):
            new_news = AddNews(None, 'text1')
            assert new_news.add_news() == 'Произошла ошибка!'

        def test_add_news_none_text(self):
            new_news = AddNews('title1', None)
            assert new_news.add_news() == 'Произошла ошибка!'

        def tearDown(self):
            db.session.remove()
            db.drop_all()


    class RecordModelCase(unittest.TestCase):
        def setUp(self):
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
            db.create_all()

        def test_new_record(self):
            new_diagnosis = RecordBuild().build()
            new_diagnosis.save_to_db()
            assert new_diagnosis.rec_login == 'login1'
            assert new_diagnosis.rec_diag == 'record1'

        def test_add_diagnosis(self):
            new_diagnosis = AddDiagnosis()
            result = new_diagnosis.add_diagnosis('login1', 'record1')
            assert result == 'doctor_space'

        def test_add_none_login(self):
            new_diagnosis = AddDiagnosis()
            result = new_diagnosis.add_diagnosis(None, 'record1')
            assert result == 'Произошла ошибка!'

        def test_add_none_diagnosis(self):
            new_diagnosis = AddDiagnosis()
            result = new_diagnosis.add_diagnosis('login1', None)
            assert result == 'Произошла ошибка!'

        def test_find_record(self):
            new_diagnosis = AddDiagnosis()
            new_diagnosis.add_diagnosis('login1', 'record1')

            diagnosis = AddDiagnosis()
            rec = diagnosis.find_record('login1')
            assert rec != None

        def test_find_None_record(self):
            new_diagnosis = AddDiagnosis()
            new_diagnosis.add_diagnosis('login1', 'record1')

            diagnosis = AddDiagnosis()
            rec = diagnosis.find_record('login2')
            assert rec == None

        def tearDown(self):
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
