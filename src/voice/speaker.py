import io
import threading

import pyaudio
import speech_recognition as sr
from src.core.deprecated_chatbot import ChatBot
from src.voice.engine import Engine, PyttsxEngine

RATE = 44100
CHUNK = 3024
FORMAT = pyaudio.paInt16
SAMPLE_WIDTH = pyaudio.get_sample_size(FORMAT)


class RecordThread(threading.Thread):

    def __init__(self, pa, callback):
        super(RecordThread, self).__init__()
        self._stop_event = threading.Event()
        self.audio = None
        self._pa = pa
        self.callback = callback

    def stop(self):
        self._stop_event.set()

    # def join(self, *args, **kwargs):
    #     self.stop()
    #     super(RecordThread,self).join(*args, **kwargs)

    def run(self):
        frames = io.BytesIO()
        stream = self._pa.open(format=FORMAT, channels=1,
                               rate=RATE,
                               input=True,
                               frames_per_buffer=CHUNK)
        while not self._stop_event.is_set():
            buffer = stream.read(CHUNK, exception_on_overflow=False)
            frames.write(buffer)
            print("* recording")

        stream.close()
        frame_data = frames.getvalue()
        frames.close()

        self.audio = sr.AudioData(frame_data, RATE, SAMPLE_WIDTH)
        self.callback(self.audio)


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


class CustomSpeaker:

    def __init__(self, chatbot: ChatBot, engine: Engine = PyttsxEngine(), signal=None):
        self.isrecording = False
        self._pa = pyaudio.PyAudio()
        self._engine = engine
        self._chatbot = chatbot
        self._recognizer = sr.Recognizer()
        self._audio = None

        self._signal = signal
        self.thread: RecordThread = None

    def recognize(self):
        if self._audio:
            try:
                text = self._recognizer.recognize_google(self._audio, language="ru-RU").lower()
                return text
            except (sr.UnknownValueError, sr.RequestError):
                return "Попробуйте ещё раз"
            # finally:
            #     self._audio = None

    def record(self):
        self._engine.talk("Говорите")
        self.isrecording = True
        frames = io.BytesIO()
        stream = self._pa.open(format=FORMAT, channels=1,
                               rate=RATE,
                               input=True,
                               frames_per_buffer=CHUNK)
        while self.isrecording:
            buffer = stream.read(CHUNK, exception_on_overflow=False)
            frames.write(buffer)
            print("* recording")

        stream.close()
        frame_data = frames.getvalue()
        frames.close()

        self._audio = sr.AudioData(frame_data, RATE, SAMPLE_WIDTH)

    def thread_rec(self):
        self.isrecording = True
        self.thread = RecordThread(self._pa, self._thread_callback)
        self.thread.start()
        self._engine.talk("Говорите")

    def _thread_callback(self, audio):
        self._audio = audio
        text = self.recognize()
        self._signal.emit(text)

    def thread_stop(self):
        self.thread.stop()
        self.isrecording = False

    def stop(self):
        self.isrecording = False

    def ask(self, question=None):
        if not question and self._audio:
            question = self.recognize()

        answer = self._chatbot.ask(question)
        self._engine.talk(answer)
        return answer


