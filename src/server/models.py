from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.serializer import Serializer

db = SQLAlchemy()


class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(20), primary_key=True, unique=True)

    # def __init__(self, id):
    #     self.id = id


class UserDialogModel(db.Model):
    __tablename__ = 'user_dialog'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(1024), nullable=False)
    answer = db.Column(db.String(1024), nullable=False)

    # def __init__(self, id, user_id, question, answer):
    #     self.id = id
    #     self.user_id = user_id
    #     self.question = question
    #     self.answer = answer


class QAModel(db.Model):
    __tablename__ = 'qa'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    question = db.Column(db.String(1024))
    answer = db.Column(db.String(1024))

    # def __init__(self, id, question, answer):
    #     self.id = id
    #     self.question = question
    #     self.answer = answer


class QuestionsModel(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(1024))

    # def __init__(self,  user_id, question):
    #     self.user_id = user_id
    #     self.question = question
