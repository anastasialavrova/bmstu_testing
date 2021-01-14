from datetime import date, datetime
from flask_login import UserMixin

from tests.unit import db

class News(db.Model):
    __tablename__ = 'news'
    id_news = db.Column(db.Integer, primary_key = True)
    news_date = db.Column(db.Date, default=datetime.utcnow)
    news_title = db.Column(db.String(300), nullable = True)
    news_text = db.Column(db.Text, nullable = True)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return ('ok')
        except:
            return ('error')

    def __repr__(self):
        return '<News %r>' % self.id_news

class User(db.Model, UserMixin):
    __tablename__= 'sign_up'
    id_sign = db.Column(db.Integer, primary_key=True)
    sign_login = db.Column(db.String(100), nullable = True, unique = True)
    sign_password = db.Column(db.String(100), nullable=True)
    sign_role = db.Column(db.Integer, nullable=True)

    def save_to_db(self):
        if self.sign_login and self.sign_password and self.sign_role:
            db.session.add(self)
            db.session.commit()
            return ('ok')
        else:
            return ('error')

    def get_id(self):
        return (self.id_sign)

class Doctors(db.Model):
    __tablename__ = 'doctors'
    id_doc = db.Column(db.Integer, primary_key = True)
    doc_name = db.Column(db.String(100), nullable = True)
    doc_spec = db.Column(db.String(100), nullable=True)
    doc_about = db.Column(db.Text, nullable=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Doctors %r>' % self.id_doc

class Record(db.Model):
    __tablename__ = 'record'
    id_rec = db.Column(db.Integer, primary_key = True)
    rec_login = db.Column(db.String(100), nullable = True)
    rec_date = db.Column(db.Date, default=datetime.utcnow)
    rec_diag = db.Column(db.Text, nullable = True)

    def __init__(self, rec_login, rec_diag):
        self.rec_login = rec_login
        self.rec_diag = rec_diag

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Record %r>' % self.id_rec


