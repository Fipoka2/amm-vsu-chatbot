from flask import Flask, jsonify, make_response, request, abort
from src.server.pool import BotPool

BOTS_COUNT = 10
botpool = None

app = Flask(__name__)


@app.route('/bot/api/v1.0/ask', methods=['POST'])
def ask():
    if not request.json or not 'question' in request.json:
        abort(400)
    bot = botpool.acquire()
    answer = bot.ask(request.json["question"])
    botpool.release(bot)
    return jsonify({'answer': answer})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def run():
    botpool = BotPool(BOTS_COUNT)
    app.run(debug=True)


if __name__ == '__main__':
    run()
