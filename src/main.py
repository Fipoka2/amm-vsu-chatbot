from src.core.chatbot import AmmChatBot
from src.voice.speaker import Speaker
from src.voice.engine import PyttsxEngine

chatbot = AmmChatBot()
engine = PyttsxEngine()
speaker = Speaker(engine, chatbot)

speaker.run()
