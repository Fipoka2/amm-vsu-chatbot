from src.core.chatbot import AmmChatBot


class BotPool:
    def __init__(self, size):
        self._bots = [AmmChatBot(path="../core/model") for _ in range(size)]

    def acquire(self):
        return self._bots.pop()

    def release(self, bot):
        self._bots.append(bot)
