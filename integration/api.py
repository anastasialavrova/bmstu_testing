from flasgger.utils import swag_from
from flask import jsonify
from flask import request
from flask_restplus import Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity,  get_raw_jwt)


from clinic import app, api, login_manager
from clinic.models import News, Doctors, Record, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class AddNews:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def add_news(self):
        new_news = News(news_title=self.title, news_text=self.text)
        try:
            app.session.add(new_news)
            app.session.commit()
        except:
            return "Произошла ошибка!"

class NewsAPI(Resource):

    @swag_from("news_json_post.yml")
    def post(self):
        title = request.args.get("news_title")
        text = request.args.get("news_text")
        news = AddNews(title, text)
        news.add_news()
        return jsonify({
            "title": title,
            "text": text
        })

    @swag_from("news_json_get.yml")
    def get(self):
        news = News.query.all()
        return {'message': 'List of news'}


class DoctorsAPI(Resource):
    @swag_from("doctors_json_get.yml")
    def get(self):
        doc = Doctors.query.all()
        return {'message': 'List of doctors'}


class Doctors_patchAPI(Resource):
    @swag_from("doctors_json_patch.yml")
    def patch(self):
        search_id = int(request.args.get("id"))
        text = str(request.args.get("text"))
        doc = Doctors.query.filter_by(id_doc=search_id).first()
        doc.doc_about += text
        try:
            doc.save_to_db()
            doc = Doctors.query.filter_by(id_doc=search_id).first()
            return jsonify({
                "doc_about": doc.doc_about
            })
        except:
            return "error"
        return jsonify({
            "id": search_id,
            "text": doc.doc_about
        })

class AddDiagnosis:
    def add_diagnosis(self, login_patient, diagnosis):
        new_diagnosis = Record(rec_login=login_patient, rec_diag=diagnosis)
        try:
            app.session.add(new_diagnosis)
            app.session.commit()
            return 'doctor_space'
        except:
            return "Произошла ошибка!"

    def find_in_db(self, login):
        return Record.query.filter_by(rec_login=login).all()

    def find_record(self, login, find_in_db):
        rec = find_in_db(login)
        return rec

class RecordAPI(Resource):
    @swag_from("record_json_post.yml")
    # @jwt_required
    def post(self):
        login_patient = request.args.get("rec_login")
        diagnosis = request.args.get("rec_diag")

        new_diagnosis = AddDiagnosis()
        new_diagnosis.add_diagnosis(login_patient, diagnosis)

        return jsonify({
            "login_patient": login_patient,
            "diagnosis": diagnosis
        })

class Record_getAPI(Resource):
    @swag_from("record_json_get.yml")
    def get(self):
        return "Ok"


class Users:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def find_in_db(self, login):
        return User.query.filter_by(sign_login = login).first()

    def sign_up(self, find_in_db):
        if self.login and self.password:
            user = find_in_db(self.login)
            if user and check_password_hash(user.sign_password, self.password):
                # login_user(user)
                if user.sign_role == 1:
                    global username
                    username = self.login
                    return 'user_space'
                elif user.sign_role == 2:
                    return 'doctor_space'
                elif user.sign_role == 3:
                    return 'admin_space'
            else:
                return 'Неправильный логин или пароль!'
        else:
            return 'Нет логина или пароля!'

    def registration(self, password, role):
        hash_password = generate_password_hash(self.password)
        new_user = User(sign_login = self.login, sign_password = hash_password, sign_role = role)
        app.session.add(new_user)
        app.session.commit()



class UserAPI_login(Resource):
    @swag_from("user_json.yml")
    def post(self):
        data = parser.parse_args()
        password = data['password']
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        if check_password_hash(current_user.sign_password, password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {'message': 'Logged in as {}'.format(current_user.sign_login),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
        else:
            return {'message': 'Wrong credentials'}
        return data

class UserAPI_registration(Resource):
    @swag_from("user_json.yml")
    def post(self):
        data = parser.parse_args()
        login = data['username']
        password = data['password']
        role = 1

        if User.find_by_username(login):
            return {'message': 'User {} already exists'.format(data['username'])}

        hash_password = generate_password_hash(password)
        new_user = User(sign_login=login, sign_password=hash_password, sign_role=role)
        try:
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            new_user.save_to_db()
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500
        return data


class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 'user_space :)'
        }

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}





## Api resource routing
api.add_resource(NewsAPI, '/news')
api.add_resource(DoctorsAPI, '/doctors')
api.add_resource(Doctors_patchAPI, '/doctors/id')
api.add_resource(RecordAPI, '/records')
api.add_resource(Record_getAPI, '/records/id')
api.add_resource(UserAPI_login, '/user_login')
api.add_resource(UserAPI_registration, '/user_registration')
api.add_resource(AllUsers, '/users')
api.add_resource(SecretResource, '/secret')
api.add_resource(TokenRefresh, '/token/refresh')


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='127.0.0.1', port=5001)
    # app.run(host='127.0.0.1', port=5002)