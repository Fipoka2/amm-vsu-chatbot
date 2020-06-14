from PyQt5.QtCore import pyqtSignal, QObject

import src.gui.design as design
import sys
from PyQt5 import QtWidgets
import src.voice.speaker as sp
from src.core.deprecated_chatbot import DeprecatedAmmChatBot


class ThreadSignal(QObject):
    signal = pyqtSignal(str)


class ChatBotApp(QtWidgets.QMainWindow, design.Ui_mainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.speaker = sp.CustomSpeaker(DeprecatedAmmChatBot('src/core/model'))
        self.sendButton.clicked.connect(self._send)
        self.speakButton.clicked.connect(self._record)
        self._update_button_style()
        signal = ThreadSignal()
        signal.signal.connect(self._update)
        self.speaker._signal = signal.signal

    def _send(self):
        text = self.messageBox.text()
        self.listWidget.addItem("Вы: " + text)
        answer = self.speaker.ask(text)
        self.listWidget.addItem("Бот: " + answer)

    def _record(self):
        if self.speaker.isrecording:
            self.sendButton.setEnabled(True)
            self.speaker.thread_stop()
        else:
            self.sendButton.setEnabled(False)
            self.speaker.thread_rec()
        self._update_button_style()

    def _recognize(self):
        text = self.speaker.recognize()
        self.messageBox.setText(text)

    def _update(self, text):
        self.messageBox.setText(text)

    def _update_button_style(self):
        if self.speaker.isrecording:
            self.speakButton.setText("стоп")
        else:
            self.speakButton.setText("запись")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ChatBotApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
