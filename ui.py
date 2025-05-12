# -*- coding:utf-8 -*-
# PyQt5로 Ui 구동하는 코드임

from PyQt5 import QtWidgets, uic
import os

# 기타 코드 클래스 임포트
from tests import Tests



class Ui(QtWidgets.QMainWindow):
    def __init__(self, path): # 초기 실행
        print("Tomatoma(ui.py->Ui): Ui 클래스 Init")
        super(Ui, self).__init__()
        uic.loadUi("./resources/ui/main.ui", self) # main.ui 불러오기

        self.tests = Tests()
        self.tests.add(os.path.join(path, 'resources/userdata'),'생명 어카노','ㄹㅇ 조짐','오늘','내일','생명과학 I')

        self.show() # 불러온 ui 보여주기

        self.path = path