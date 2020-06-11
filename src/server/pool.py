from src.core.chatbot import AmmChatBot
from src.core.chatbot2 import NewAmmChatBot


class BotPool:
    def __init__(self, size):
        self._bots = [NewAmmChatBot(path="src/core/model") for _ in range(size)]

    def acquire(self):
        return self._bots.pop()

    def release(self, bot):
        self._bots.append(bot)
