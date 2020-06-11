from src.core.chatbot import AmmChatBot

a = AmmChatBot(path="model")
print(a._agent(["справка что я учусь на пэ эм эм"], [0]))
