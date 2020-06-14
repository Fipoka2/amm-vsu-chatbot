import string
from random import random

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(20), primary_key=True, unique=True)

    @staticmethod
    def generate_id():
        return ''.join(random.SystemRandom().
                       choice(string.ascii_uppercase + string.digits) for _ in range(20))


class UserDialogModel(db.Model):
    __tablename__ = 'user_dialog'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(1024), nullable=False)
    answer = db.Column(db.String(1024), nullable=False)


class QAModel(db.Model):
    __tablename__ = 'qa'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    question = db.Column(db.String(1024))
    answer = db.Column(db.String(1024))


class QuestionsModel(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(1024))
