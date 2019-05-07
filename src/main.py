from src.chatbot import AmmChatBot
from src.speaker import Speaker, PyttsxEngine

chatbot = AmmChatBot()
engine = PyttsxEngine()
speaker = Speaker(engine, chatbot)

speaker.run()
