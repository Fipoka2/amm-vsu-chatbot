from flask import Flask, jsonify, make_response, request, abort
from flask.json import JSONEncoder
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta

import src.server.routing as routing
from src.core.chatbot2 import NewAmmChatBot
from src.server.db_provider import UserProvider
from src.server.models import UsersModel, db, QuestionsModel, UserDialogModel
from src.server.pool import BotPool


class ExtendedJSONEncoder(JSONEncoder):

    @staticmethod
    def _encode_model(obj):
        return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return self._encode_model(obj)

        return super(ExtendedJSONEncoder, self).default(obj)


chatbot = NewAmmChatBot("src/core/data/dataset_vsu_qa.csv")

app = Flask(__name__)
app.json_encoder = ExtendedJSONEncoder
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/chatbot"
db.init_app(app)


def run(dev: bool = False):
    if dev:
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(debug=False)


@app.route(routing.ASK_QUESTION, methods=['POST'])
def ask():
    user_id = request.headers.get('user_id')
    if user_id is None:
        abort(403)
    if not request.json or not 'question' in request.json:
        abort(400)
    question = request.json["question"]
    answer, valid = chatbot.ask(question)

    try:
        db.session.add(UserDialogModel(user_id=user_id, answer=answer, question=question))
        if not valid:
            u = QuestionsModel(user_id, question)
            db.session.add(u)

        db.session.commit()
        return jsonify({'answer': answer})
    except SQLAlchemyError as err:
        print(err)
        return make_response(jsonify({'error': 'Internal server error'}), 500)


@app.route(routing.NEW_USER, methods=['GET'])
def create_user():
    user_id = UserProvider.add_user()
    return jsonify({
        'user_id': user_id
    })


@app.route(routing.DIALOG_ROUTE, methods=['GET'])
def get_dialog():
    user_id = request.headers.get('user_id')
    if user_id is None:
        abort(403)

    dialog = db.session.query(UserDialogModel).filter(UserDialogModel.user_id == user_id).all()
    return jsonify(dialog)


@app.route(routing.DIALOG_ROUTE, methods=['DELETE'])
def delete_dialog():
    user_id = request.headers.get('user_id')
    if user_id is None:
        abort(403)

    UserDialogModel.query.filter(UserDialogModel.user_id == user_id).delete()
    db.session.commit()
    return jsonify(success=True)


@app.errorhandler(404)
def not_found(error):
    print(UsersModel.query.all())
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    run()
