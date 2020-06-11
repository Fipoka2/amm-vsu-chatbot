from src.server.entity import Dialog


class UserProvider:
    @staticmethod
    def add_user():
        user_id = '435345353'
        return user_id


class DialogProvider:
    @staticmethod
    def delete_dialog(user_id: str):
        dialog = []
        return True

    @staticmethod
    def add_question(question: str):
        return True

    @staticmethod
    def add_qa(user_id: str, question: str, answer: str):
        return True

    @staticmethod
    def get_dialog(user_id: str) -> Dialog:
        dialog = Dialog()
        return dialog
