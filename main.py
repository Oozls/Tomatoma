# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets
import sys

from ui import Ui

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()