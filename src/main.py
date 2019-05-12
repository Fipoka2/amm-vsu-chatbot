from src.chatbot import AmmChatBot
from src.speaker import Speaker
from src.engine import PyttsxEngine

chatbot = AmmChatBot()
engine = PyttsxEngine()
speaker = Speaker(engine, chatbot)

speaker.run()
