# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(661, 481)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setMinimumSize(QtCore.QSize(0, 31))
        self.sendButton.setObjectName("sendButton")
        self.gridLayout.addWidget(self.sendButton, 1, 2, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 3)
        self.messageBox = QtWidgets.QLineEdit(self.centralwidget)
        self.messageBox.setMinimumSize(QtCore.QSize(471, 31))
        self.messageBox.setObjectName("messageBox")
        self.gridLayout.addWidget(self.messageBox, 1, 0, 1, 1)
        self.speakButton = QtWidgets.QPushButton(self.centralwidget)
        self.speakButton.setMinimumSize(QtCore.QSize(0, 31))
        self.speakButton.setObjectName("speakButton")
        self.gridLayout.addWidget(self.speakButton, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.sendButton.setText(_translate("mainWindow", "отправить"))
        self.speakButton.setText(_translate("mainWindow", "запись"))


