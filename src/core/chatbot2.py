from deeppavlov import configs, train_model
from deeppavlov.core.common.file import read_json

from src.core.chatbot import ChatBot


class FallbackMessage:
    def __init__(self, threshold: float, message="Пожалуйста, перефразируйте вопрос."):
        if threshold > 1.0:
            threshold = 1
        if threshold < 0.0:
            threshold = 0
        self.threshold = threshold
        self.message = message


class NewAmmChatBot(ChatBot):
    def __init__(self, data_path: str = "data/dataset_vsu_qa.csv",
                 fallback: FallbackMessage = FallbackMessage(0.7)):
        self._fallback = fallback
        model_config = read_json(configs.faq.tfidf_logreg_autofaq)
        model_config["dataset_reader"]["data_path"] = data_path
        model_config["dataset_reader"]["data_url"] = None
        self._faq = train_model(model_config)

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

