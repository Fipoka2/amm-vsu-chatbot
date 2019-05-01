import speech_recognition as sr
import os
import sys
import pyttsx3
from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector


def talk(words):
    print(words)
    if os.name == 'nt':
        engine = pyttsx3.init()
        engine.say(words)
        engine.runAndWait()
    else:
        os.system("say " + words)


def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        talk("Ожидайте")
        question = r.recognize_google(audio, language="ru-RU").lower()
        if question == 'выход':
            talk("Пока")
            sys.exit()
        answer = agent([question], [0])
        talk(answer)
    except sr.UnknownValueError:
        talk("Я вас не поняла")
        question = command()
    return question


faq = SimilarityMatchingSkill(data_path='dataset_vsu_qa.csv',
                              x_col_name='Question',
                              y_col_name='Answer',
                              save_load_path='./model',
                              config_type='tfidf_autofaq',
                              edit_dict={},
                              train=False)

hello = PatternMatchingSkill(responses=['Привет', 'Приветствую'],
                             patterns=['Привет', 'Здравствуйте'])
bye = PatternMatchingSkill(responses=['Пока', 'Всего доброго'], patterns=['Пока', 'До свидания'])
fallback = PatternMatchingSkill(responses=['Пожалуйста перефразируйте'], default_confidence=0.3)

agent = DefaultAgent([hello, bye, faq, fallback], skills_selector=HighestConfidenceSelector())

talk("Привет, чем я могу помочь вам?")

while True:
    command()
