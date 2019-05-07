import abc

import pyttsx3
import speech_recognition as sr

from src.chatbot import ChatBot


class Engine(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def talk(self, text):
        pass


class PyttsxEngine(Engine):

    def __init__(self):
        super().__init__()
        self._engine = pyttsx3.init()
        self._engine.setProperty('voice', 'russian')
        self._engine.setProperty('rate', 100)

    def talk(self, text):
        self._engine.say(text)
        self._engine.runAndWait()


class Speaker:
    def __init__(self, engine: Engine, chatbot: ChatBot):
        self._engine = engine
        self._recognizer = sr.Recognizer()
        self._chatbot = chatbot

    def _ask(self) -> bool:
        with sr.Microphone() as source:
            print("Говорите")
            self._recognizer.pause_threshold = 1
            self._recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = self._recognizer.listen(source)
        try:
            self._engine.talk("Ожидайте")
            question = self._recognizer.recognize_google(audio, language="ru-RU").lower()
            if question == 'выход':
                self._engine.talk("Пока")
                return False

            answer = self._chatbot.ask(question)
            self._engine.talk(answer)
        except sr.UnknownValueError:
            self._engine.talk("Я вас не поняла")
        return True

    def run(self):
        state = True
        while state:
            state = self._ask()
