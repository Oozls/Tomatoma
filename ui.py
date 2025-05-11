# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets, uic
import os

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./resources/ui/main.ui")
        self.show()