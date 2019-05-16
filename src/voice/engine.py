import abc
import subprocess
import pyttsx3


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


class RHVoiceEngine(Engine):
    DEFAULT_VOICE = 'anna'

    def __init__(self):
        super().__init__()


    def talk(self, text):
        # subprocess.run(["say ", text])
        pass
