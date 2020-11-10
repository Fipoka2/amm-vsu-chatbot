import abc

from deeppavlov import train_model, build_model, configs
from deeppavlov.core.common.file import read_json

from nltk.corpus import stopwords

class ChatBot(abc.ABC):

    @abc.abstractmethod
    def ask(self, question: str) -> str:
        pass


class FallbackMessage:
    def __init__(self, threshold: float, message="Пожалуйста, перефразируйте вопрос."):
        if threshold > 1.0:
            threshold = 1
        if threshold < 0.0:
            threshold = 0
        self.threshold = threshold
        self.message = message


class AmmChatBot(ChatBot):

    def __init__(self, config_path: str = "src/core/configs/tfidf_logreg_autofaq.json",
                 data_path: str = None, train: bool = True,
                 fallback: FallbackMessage = FallbackMessage(0.7)):
        self._fallback = fallback

        stop_words = stopwords.words('russian')
        stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])

        model_config = read_json(config_path)
        if data_path:
            model_config["dataset_reader"]["data_path"] = data_path
            model_config["dataset_reader"]["data_url"] = None
        if train:
            model_config["chainer"]["pipe"][4]["warm_start"] = True
            model_config["chainer"]["pipe"][0]["stopwords"] = stop_words
            self._faq = train_model(model_config)
        else:
            self._faq = build_model(model_config)

    def ask(self, question: str):
        answers, probability = self._faq([question])
        valid = self._check_similarity(probability[0], self._fallback.threshold)
        if valid:
            return answers[0], True
        else:
            return self._fallback.message, True

    @staticmethod
    def _check_similarity(arr: list, threshold: float) -> bool:
        max_value = max(arr)
        print(max_value)
        if max_value < threshold:
            return False
        else:
            return True
