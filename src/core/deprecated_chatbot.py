
import abc

from deeppavlov.deprecated.agents.default_agent import DefaultAgent
from deeppavlov.deprecated.agents.processors import HighestConfidenceSelector

from deeppavlov.deprecated.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.deprecated.skills.similarity_matching_skill import SimilarityMatchingSkill





class DeprecatedAmmChatBot(ChatBot):
    def __init__(self, path):
        faq = SimilarityMatchingSkill(data_path='data/dataset_vsu_qa.csv',
                                      x_col_name='Question',
                                      y_col_name='Answer',
                                      save_load_path=path,
                                      config_type='tfidf_autofaq',
                                      edit_dict={},
                                      train=False)

        hello = PatternMatchingSkill(responses=['Привет', 'Приветствую'],
                                     patterns=['Привет', 'Здравствуйте'])
        bye = PatternMatchingSkill(responses=['Пока', 'Всего доброго'],
                                   patterns=['Пока', 'До свидания'])
        fallback = PatternMatchingSkill(responses=['Пожалуйста перефразируйте'],
                                        default_confidence=0.3)

        self._dialog = []
        self._agent = DefaultAgent([hello, bye, faq, fallback],
                                   skills_selector=HighestConfidenceSelector())

    def ask(self, question: str):
        answers = self._agent([question], [0])
        self._dialog.append((question, answers[0]))
        return answers

    def get_dialog(self) -> list:
        return self._dialog
