from flask import Flask, jsonify, make_response, request, abort
from src.server.pool import BotPool

BOTS_COUNT = 10
botpool = None

app = Flask(__name__)


def run(dev: bool = False):
    botpool = BotPool(BOTS_COUNT)
    if dev:
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(debug=False)


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


if __name__ == '__main__':
    run()
