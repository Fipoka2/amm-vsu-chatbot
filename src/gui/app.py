from PyQt5.QtCore import QThread

import src.gui.design as design
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import src.speaker as sp
from src.chatbot import AmmChatBot


class ChatBotApp(QtWidgets.QMainWindow, design.Ui_mainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.speaker = sp.CustomSpeaker(AmmChatBot('../model'))
        self.sendButton.clicked.connect(self._send)
        self.speakButton.clicked.connect(self._record)

    def _send(self):
        text = self.messageBox.text()
        self.listWidget.addItem("Вы: " + text)
        answer = self.speaker.ask(text)
        self.listWidget.addItem("Бот: " + answer)

    def _record(self):
        if self.speaker.isrecording:
            self.speaker.thread_stop()
        else:
            self.speaker.thread_rec(self._recognize)

    def _recognize(self, audio):
        self.speaker._audio = audio
        text = self.speaker.recognize()
        self.messageBox.setText(text)



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ChatBotApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()

