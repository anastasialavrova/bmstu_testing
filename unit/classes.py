from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user



from env import app, login_manager
from models import News, Doctors, Record, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class AddNews:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def add_news(self):
        new_news = News(news_title=self.title, news_text=self.text)

        if self.title and self.text:
            new_news.save_to_db()
            return 'ok'
        else:
            return "Произошла ошибка!"


class AddDiagnosis:
    def add_diagnosis(self, login_patient, diagnosis):
        new_diagnosis = Record(rec_login=login_patient, rec_diag=diagnosis)
        if login_patient and diagnosis:
            new_diagnosis.save_to_db()
            return 'doctor_space'
        else:
            return "Произошла ошибка!"

    def find_in_db(self, login):
        return Record.query.filter_by(rec_login=login).all()

    def find_record(self, login):
        rec = self.find_in_db(login)
        if rec:
            return rec
        else:
            return None


class Users:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def check_hash(self, password1, password2):
        print(password1, password2)
        print(check_password_hash(password1, password2))
        return check_password_hash(password1, password2)

    def find_in_db(self, login):
        return User.query.filter_by(sign_login = login).first()

    def sign_in(self, check_hash):
        if self.login and self.password:
            user = User.query.filter_by(sign_login = self.login).first()
            if user and check_hash(user.sign_password, self.password):
                if user.sign_role == 1:
                    global username
                    username = self.login
                    return 'user_space'
                elif user.sign_role == 2:
                    return 'doctor_space'
                elif user.sign_role == 3:
                    return 'admin_space'
            else:
                return('Неправильный логин или пароль!')
        else:
            return ('Нет логина или пароля!')

    def registration(self, password2, role):
        if not self.login or not self.password or not password2:
            return('Заполните все поля!')
        elif self.password != password2:
            return('Пароли не совпадают')
        else:
            hash_password = generate_password_hash(self.password)
            new_user = User(sign_login = self.login, sign_password = hash_password, sign_role = role)
            try:
                new_user.save_to_db()
                return 'ok'
            except:
                return 'error'

