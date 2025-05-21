# -*- coding:utf-8 -*-
# PyQt5로 Ui 구동하는 코드임

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QWidget
from PyQt5.QtCore import Qt
import os

# 기타 코드 클래스 임포트
from tests import Tests



class Ui(QtWidgets.QMainWindow):
    def __init__(self, path): # 초기 실행
        print("Tomatoma (ui.py->Ui): Ui 클래스 Init")
        super(Ui, self).__init__()
        uic.loadUi("./resources/ui/main.ui", self) # main.ui 불러오기

        self.tests = Tests()
        self.tests.add(os.path.join(path, 'resources/userdata'),'생명 어카노','ㄹㅇ 조짐','오늘','내일','생명과학 I')


        #변수 설정
        self.menuToggle = False


        #요소 지정
        self.mainContainer = self.findChild(QStackedWidget, 'mainContainer')
        self.mainContainer.setCurrentIndex(0)
        self.mainSidebar = self.findChild(QWidget, 'mainSidebar')
        self.menuBtn = self.findChild(QPushButton, 'menuBtn')
        self.homeBtn = self.findChild(QPushButton, 'homeBtn')
        self.testsBtn = self.findChild(QPushButton, 'testsBtn')


        #이벤트 지정
        self.menuBtn.clicked.connect(self.toggleMenu)
        self.homeBtn.clicked.connect(lambda: self.mainContainer.setCurrentIndex(0))
        self.testsBtn.clicked.connect(lambda: self.mainContainer.setCurrentIndex(1))


        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show() # 불러온 ui 보여주기

        self.path = path


    def toggleMenu(self):
        if self.menuToggle: self.mainSidebar.setMaximumWidth(50)
        else: self.mainSidebar.setMaximumWidth(200)
        self.menuToggle = not self.menuToggle