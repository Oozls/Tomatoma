# -*- coding:utf-8 -*-
# PyQt5로 Ui 구동하는 코드임

from PyQt5 import QtWidgets, uic, sip
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QWidget, QDateEdit, QTimeEdit, QComboBox, QTextEdit, QLineEdit, QMessageBox, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime, QSize
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta
import os, time

# 기타 코드 클래스 임포트
import tests, search



class Ui(QtWidgets.QMainWindow):
    def __init__(self, path): # 초기 실행
        print("Tomatoma (ui.py->Ui): Ui 클래스 Init")
        super(Ui, self).__init__()
        uic.loadUi("./resources/ui/main.ui", self) # main.ui 불러오기


        #변수 설정
        self.menuToggle = False


        #요소 지정
        self.mainContainer = self.findChild(QStackedWidget, 'mainContainer')
        self.mainContainer.setCurrentIndex(0)
        self.mainSidebar = self.findChild(QWidget, 'mainSidebar')

        self.menuBtn = self.findChild(QPushButton, 'menuBtn')
        self.homeBtn = self.findChild(QPushButton, 'homeBtn')
        self.testsBtn = self.findChild(QPushButton, 'testsBtn')
        self.closeBtn = self.findChild(QPushButton, 'closeBtn')

        self.testsSearchInput = self.findChild(QLineEdit, 'testsSearchInput')
        self.testsScrollAreaContainer = self.findChild(QWidget, 'testsScrollAreaContainer')
        self.testsSearchSample = self.findChild(QWidget, 'testsSearchSample')
        self.testsSearchSample.hide()

        self.testsAddEnterBtn = self.findChild(QPushButton, 'testsAddEnterBtn')
        self.testsAddNameInput = self.findChild(QLineEdit, 'testsAddNameInput')
        self.testsAddDescInput = self.findChild(QTextEdit, 'testsAddDescInput')
        self.testsAddSubjectInput = self.findChild(QComboBox, 'testsAddSubjectInput')
        self.testsAddDateInput = self.findChild(QDateEdit, 'testsAddDateInput')
        self.testsAddTimeInput = self.findChild(QTimeEdit, 'testsAddTimeInput')
        self.testsAddBtn = self.findChild(QPushButton, 'testsAddBtn')


        #이벤트 지정
        #self.menuBtn.clicked.connect(self.toggleMenu) 검색 시 나오는 위젯 크기 조절이 귀찮아서 그냥 기능을 없앴습니다 머리 아파요
        self.homeBtn.clicked.connect(lambda: self.mainContainer.setCurrentIndex(0)) #lambda가 뭔지는 모르겠지만 일단 작동함
        self.closeBtn.clicked.connect(self.close)
        self.testsBtn.clicked.connect(lambda: self.mainContainer.setCurrentIndex(1))
        self.testsBtn.clicked.connect(self.testsSearch)
        self.testsAddEnterBtn.clicked.connect(self.testAddSetup)
        self.testsAddBtn.clicked.connect(self.testAdd)
        self.testsSearchInput.textChanged.connect(self.testsSearch)


        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show() # 불러온 ui 보여주기

        self.path = path
        self.data_path = os.path.join(self.path, 'resources/userdata')
        self.testsUpdate()


    def toggleMenu(self):
        print('Tomatoma (ui.py->Ui): toggleMenu 함수 실행')
        if self.menuToggle:
            self.mainSidebar.setMaximumWidth(50)
            for child in self.testsScrollAreaContainer.findChildren(QWidget):
                child.show()
        else:
            self.mainSidebar.setMaximumWidth(200)
            for child in self.testsScrollAreaContainer.findChildren(QWidget):
                child.hide()

        self.menuToggle = not self.menuToggle

    
    def testAddSetup(self):
        print('Tomatoma (ui.py->Ui): testsAddSetup 함수 실행')
        # 텍스트 리셋
        self.testsAddNameInput.setText('')
        self.testsAddDescInput.setText('')

        self.testsAddSubjectInput.clear()
        self.testsAddSubjectInput.addItem('국어')
        self.testsAddSubjectInput.addItem('영어')
        self.testsAddSubjectInput.addItem('수학')
        self.testsAddSubjectInput.addItem('정보과학')

        self.testsAddDateInput.setDate(QDate.currentDate())
        self.testsAddTimeInput.setTime(QTime(0,0))
        
        self.mainContainer.setCurrentIndex(2) # 페이지 이름으로 넘기는 기능 왜 없냐


    def testAdd(self):
        print('Tomatoma (ui.py->Ui): testAdd 함수 실행')
        if self.testsAddNameInput.text().replace(' ','') == '':
            QMessageBox.about(self, "에러", "이름을 입력해주세요.")
            print('Tomatoma (ui.py->Ui): 이름 미입력')
            return
        
        name = self.testsAddNameInput.text()
        desc = self.testsAddDescInput.toPlainText()
        subject = self.testsAddSubjectInput.currentText()
        date = self.testsAddDateInput.date()
        timeI = self.testsAddTimeInput.time()
        dateTime = QDateTime(date, timeI).toPyDateTime()
        unixDateTime = time.mktime(dateTime.timetuple())
        
        print(f'Tomatoma (ui.py->Ui): name={name}')
        print(f'Tomatoma (ui.py->Ui): desc={desc}')
        print(f'Tomatoma (ui.py->Ui): subject={subject}')
        print(f'Tomatoma (ui.py->Ui): date={date}')
        print(f'Tomatoma (ui.py->Ui): timeI={timeI}')
        print(f'Tomatoma (ui.py->Ui): dateTime={time.mktime(dateTime.timetuple())}')

        tests.add(self.data_path,name,desc,unixDateTime,subject)
        print('Tomatoma (ui.py->Ui): 수행평가 일정 생성 완료')
        self.testsUpdate()
        self.mainContainer.setCurrentIndex(1)
        QMessageBox.about(self, "완료", "일정이 생성되었습니다.")


    def testsUpdate(self):
        print('Tomatoma (ui.py->Ui): testsUpdate 함수 실행')
        self.tests_list = tests.lists(self.data_path)
        print('Tomatoma (ui.py->Ui): 수행평가 일정 업데이트됨')


    def testsSearch(self):
        print('Tomatoma (ui.py->Ui): testsSearch 함수 실행')

        input_string = self.testsSearchInput.text()
        print(f'Tomatoma (ui.py->Ui): input_string={input_string}')

        result_list = []
        if input_string == '':
            result_list = self.tests_list
        else:
            result_list = search.search(input_string, self.tests_list)
        print(f'Tomatoma (ui.py->Ui): result_list={result_list}')
        
        for child in self.testsScrollAreaContainer.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()

        def _make_font(pointsize=None, bold=False):
            font = QFont("Noto Sans KR")
            if pointsize:
                font.setPointSize(pointsize)
            font.setBold(bold)
            font.setWeight(QFont.Bold if bold else QFont.Normal)
            return font

        y = 10
        for i in result_list: #검색 결과 위젯 생성하는 거임 아니 왜 pyqt5 위젯 복사 지원 안 하냐
            widget = QWidget(self.testsScrollAreaContainer)
            widget.setParent(self.testsScrollAreaContainer)
            widget.setStyleSheet('QWidget {background-color: #fefbfb;border-radius: 5px;border: 1px solid rgba(185, 185, 185, 100);}')
            widget.setGeometry(10, y, self.testsScrollAreaContainer.width()-20, 150)

            layout = QGridLayout(widget)
            # QLabel: 이름
            name = QLabel("이름")
            name.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
            name.setFont(_make_font(20, bold=True))
            name.setText(i['name'])
            layout.addWidget(name, 0, 0)

            # QLabel: 과목
            subject = QLabel("과목")
            subject.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            subject.setFont(_make_font(bold=True))
            subject.setText(i['subject'])
            layout.addWidget(subject, 0, 1)

            # QLabel: 설명
            desc = QLabel("설명")
            desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            desc.setMaximumSize(QSize(16777215, 100))
            desc.setText(i['desc'])
            layout.addWidget(desc, 1, 0)

            # QLabel: 시간
            dateTime = QLabel("날짜")
            dateTime.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
            dateTime.setText(datetime.fromtimestamp(i['enddate']).strftime("%Y-%m-%d %H:%M:%S"))
            layout.addWidget(dateTime, 2, 0)

            # QLabel: 남은 시간
            leftTime = QLabel("남은 시간")

            now = time.time()
            diff_seconds = i['enddate'] - now

            if diff_seconds < 0:
                leftTime.setText('이미 지난 수행이에요.')
            else:
                diff = timedelta(seconds=int(diff_seconds))
                days = diff.days
                hours = diff.seconds // 3600
                minutes = (diff.seconds % 3600) // 60
                seconds = diff.seconds % 60

                if days > 0:
                    leftTime.setText(f'{days}일 후')
                elif hours > 0:
                    leftTime.setText(f'{hours}시간 후')
                elif minutes > 0:
                    leftTime.setText(f'{minutes}분 후')
                else:
                    leftTime.setText(f'{seconds}초 후')

            layout.addWidget(leftTime, 2, 1)

            widget.show()

            y+=160
        
        self.testsScrollAreaContainer.setMinimumSize(0,160*len(result_list)+10)