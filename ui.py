# -*- coding:utf-8 -*-
# PyQt5로 Ui 구동하는 코드임 (사실상 메인)

from PyQt5 import QtWidgets, uic, sip #sip는 어따 쓰는 거더라
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QWidget, QDateEdit, QTimeEdit, QComboBox, QTextEdit, QLineEdit, QMessageBox, QGridLayout, QLabel, QSizePolicy, QScrollArea, QVBoxLayout
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime, QSize, QTimer
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime, timedelta
import os, time

# 기타 코드 클래스 임포트
import tests, search, alarm



class Ui(QtWidgets.QMainWindow):
    def __init__(self, path): # 초기 실행
        # print("Tomatoma (ui.py->Ui): Ui 클래스 Init")
        super(Ui, self).__init__()
        uic.loadUi("./resources/ui/main.ui", self) # main.ui 불러오기
        

        #변수 설정
        self.menuToggle = False
        self.drag_position = None


        #요소 지정
        self.mainTop = self.findChild(QWidget, 'mainTop')
        self.mainContainer = self.findChild(QStackedWidget, 'mainContainer')
        self.mainContainer.setCurrentIndex(0)
        self.mainSidebar = self.findChild(QWidget, 'mainSidebar')

        self.mainTop.mousePressEvent = self.title_mouse_press
        self.mainTop.mouseMoveEvent = self.title_mouse_move
        self.mainTop.mouseReleaseEvent = self.title_mouse_release

        self.menuBtn = self.findChild(QPushButton, 'menuBtn')
        self.homeBtn = self.findChild(QPushButton, 'homeBtn')
        self.testsBtn = self.findChild(QPushButton, 'testsBtn')
        self.closeBtn = self.findChild(QPushButton, 'closeBtn')

        self.testsSearchInput = self.findChild(QLineEdit, 'testsSearchInput')
        self.testsScrollArea = self.findChild(QScrollArea, 'testsScrollArea')
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
        self.setWindowIcon(QIcon(os.path.join(path,'resources/ui/tomato.ico')))
        self.show() # 불러온 ui 보여주기

        self.path = path
        self.data_path = os.path.join(self.path, 'resources/userdata')
        self.tests_alarm = {}
        self.testsUpdate()
        self.oldPos = self.pos()

        self.timer = QTimer()
        self.timer.timeout.connect(self.alarmCheck)
        self.timer.start(1000)


    def title_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def title_mouse_move(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def title_mouse_release(self, event):
        self.drag_position = None
        event.accept()


    # def TopMousePressEvent(self, event): # 이건 퍼옴, 드래그 가능한 창
    #     self.oldPos = event.globalPos()

    # def TopMouseMoveEvent(self, event):
    #     delta = QPoint (event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()


    # def toggleMenu(self): # 메뉴 크기 조절 함수 -> 버그 많아서 없앴음
    #     print('Tomatoma (ui.py->Ui): toggleMenu 함수 실행')
    #     if self.menuToggle:
    #         self.mainSidebar.setMaximumWidth(50)
    #         for child in self.testsScrollAreaContainer.findChildren(QWidget):
    #             child.show()
    #     else:
    #         self.mainSidebar.setMaximumWidth(200)
    #         for child in self.testsScrollAreaContainer.findChildren(QWidget):
    #             child.hide()

    #     self.menuToggle = not self.menuToggle

    
    def testAddSetup(self): # 수행평가 일정 추가 시 입력 기본값 설정 함수
        # print('Tomatoma (ui.py->Ui): testsAddSetup 함수 실행')
        # 텍스트 리셋
        self.testsAddNameInput.setText('')
        self.testsAddDescInput.setText('')

        self.testsAddSubjectInput.clear()
        self.testsAddSubjectInput.addItem('국어')
        self.testsAddSubjectInput.addItem('영어')
        self.testsAddSubjectInput.addItem('수학')
        self.testsAddSubjectInput.addItem('물리')
        self.testsAddSubjectInput.addItem('화학')
        self.testsAddSubjectInput.addItem('생명과학')
        self.testsAddSubjectInput.addItem('지구과학')
        self.testsAddSubjectInput.addItem('정보과학')
        # 문과 과목 뭐 있는지 몰라서 못 넣었습니다 + 교양

        self.testsAddDateInput.setDate(QDate.currentDate())
        self.testsAddTimeInput.setTime(QTime(0,0))
        
        self.mainContainer.setCurrentIndex(2) # 페이지 이름으로 넘기는 기능 왜 없냐


    def testAdd(self): # 진짜로 수행 일정 추가하는 일정
        # print('Tomatoma (ui.py->Ui): testAdd 함수 실행')
        if self.testsAddNameInput.text().replace(' ','') == '':
            QMessageBox.about(self, "에러", "이름을 입력해주세요.")
            # print('Tomatoma (ui.py->Ui): 이름 미입력')
            return
        
        name = self.testsAddNameInput.text()
        desc = self.testsAddDescInput.toPlainText()
        subject = self.testsAddSubjectInput.currentText()
        date = self.testsAddDateInput.date()
        timeI = self.testsAddTimeInput.time()
        dateTime = QDateTime(date, timeI).toPyDateTime()
        unixDateTime = time.mktime(dateTime.timetuple())
        
        # print(f'Tomatoma (ui.py->Ui): name={name}')
        # print(f'Tomatoma (ui.py->Ui): desc={desc}')
        # print(f'Tomatoma (ui.py->Ui): subject={subject}')
        # print(f'Tomatoma (ui.py->Ui): date={date}')
        # print(f'Tomatoma (ui.py->Ui): timeI={timeI}')
        # print(f'Tomatoma (ui.py->Ui): dateTime={time.mktime(dateTime.timetuple())}')

        tests.add(self.data_path,name,desc,unixDateTime,subject)

        new_dict = {}
        new_dict['day'] = False
        new_dict['hour'] = False
        new_dict['half'] = False
        new_dict['min'] = False
        self.tests_alarm[name] = new_dict

        # print('Tomatoma (ui.py->Ui): 수행평가 일정 생성 완료')
        self.testsUpdate()
        self.testsSearchInput.setText('')
        self.testsSearch()
        self.mainContainer.setCurrentIndex(1)
        alarm.alarm("성공!", "일정이 생성되었습니다.", self.path)


    def testsUpdate(self): # tests 코드 통해서 파일 목록 불러오고 클래스 안에 저장하는 거
        # print('Tomatoma (ui.py->Ui): testsUpdate 함수 실행')
        self.tests_list = tests.lists(self.data_path)
        # print('Tomatoma (ui.py->Ui): 수행평가 일정 업데이트됨')
        # print(f'Tomatoma (ui.py->Ui): self.tests_list={self.tests_list}')
        if len(self.tests_alarm) == 0:
            for i in self.tests_list:
                new_dict = {}
                new_dict['day'] = False
                new_dict['hour'] = False
                new_dict['half'] = False
                new_dict['min'] = False
                self.tests_alarm[i['name']] = new_dict



    def testsSearch(self): # 검색 출력하는 거임
        # print('Tomatoma (ui.py->Ui): testsSearch 함수 실행')

        input_string = self.testsSearchInput.text()
        # print(f'Tomatoma (ui.py->Ui): input_string={input_string}')

        result_list = []
        if input_string == '':
            result_list = self.tests_list
        else:
            result_list = search.search(input_string, self.tests_list)
        result_list.sort(key=lambda x: x['enddate'])

        result_list = tests.limitLists(result_list)

        # print(f'Tomatoma (ui.py->Ui): result_list={result_list}')
        
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
        if len(result_list) >= 3: width = self.testsScrollArea.width()-12
        else: width = self.testsScrollArea.width()
        for i in result_list: #검색 결과 위젯 생성하는 거임 아니 왜 pyqt5 위젯 복사 지원 안 하냐
            widget = QWidget(self.testsScrollAreaContainer)
            widget.setParent(self.testsScrollAreaContainer)
            widget.setGeometry(10, y, width-20, 200)

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
            subject.setStyleSheet('QLabel {qproperty-alignment: AlignCenter}')
            subject.setText(i['subject'])
            layout.addWidget(subject, 0, 1)

            # QLabel: 설명
            scrollArea = QScrollArea(self.testsScrollAreaContainer)
            scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            scrollArea.setMaximumSize(QSize(16777215, 100))
            scrollArea.setStyleSheet('QScrollBar:vertical {width: 12px;background: #d3d88f;} QScrollBar:horizontal {width: 12px;background: #d3d88f;} QScrollBar::handle:vertical {border: none;border-radius: 5px;background-color: #a9cb6a;min-height: 30px;} QScrollBar::handle:horizontal {border: none;border-radius: 5px;background-color: #a9cb6a;min-height: 30px;} QScrollBar::add-line, QScrollBar::sub-line {background: transparent;}')
            layout.addWidget(scrollArea, 1, 0)
            
            scrollArea.setWidgetResizable(True)

            scrollWidget = QWidget(scrollArea)
            scrollWidget.setStyleSheet('border-radius: 0px;')
            scrollArea.setStyleSheet('background-color: #fefbfb; border: 0;')
            scrollArea.setWidget(scrollWidget)

            scrollLayout = QVBoxLayout(scrollWidget)
            scrollLayout.setContentsMargins(0,0,0,0)

            desc = QLabel(scrollWidget)
            desc.setWordWrap(True)
            desc.setText(i['desc'])
            if i['desc'].replace(' ','') == '': desc.setText("...")
            desc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            scrollLayout.addWidget(desc)

            # QLabel: 시간
            dateTime = QLabel("날짜")
            dateTime.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
            dateTime.setText(datetime.fromtimestamp(i['enddate']).strftime("%Y-%m-%d %H:%M:%S"))
            layout.addWidget(dateTime, 2, 0)

            # QLabel: 남은 시간
            leftTime = QLabel("남은 시간")
            leftTime.setStyleSheet('QLabel {qproperty-alignment: AlignCenter, margin: 10px 0 10px 0}')

            now = time.time()
            diff_seconds = i['enddate'] - now

            if diff_seconds < 0:
                leftTime.setText('이미 지난 수행이에요.')
                widget.setStyleSheet('QWidget {background-color: #cfcfcf;border-radius: 5px;border: 1px solid rgba(185, 185, 185, 100);}')
                scrollWidget.setStyleSheet('background-color: #cfcfcf; border: 0;')
            else:
                widget.setStyleSheet('QWidget {background-color: #fefbfb;border-radius: 5px;border: 1px solid rgba(185, 185, 185, 100);}')
                diff = timedelta(seconds=int(diff_seconds))
                days = diff.days
                hours = diff.seconds // 3600
                minutes = (diff.seconds % 3600) // 60
                seconds = diff.seconds % 60

                if days > 0:
                    leftTime.setText(f'{days+1}일 후')
                elif hours > 0:
                    leftTime.setText(f'{hours}시간 후')
                elif minutes > 0:
                    leftTime.setText(f'{minutes}분 후')
                else:
                    leftTime.setText(f'{seconds}초 후')

            layout.addWidget(leftTime, 2, 1)

            widget.show()

            y+=210
        self.testsScrollAreaContainer.setMinimumSize(0,210*len(result_list)+10)


    def alarmCheck(self): #전송
        # print('Tomatoma (ui.py->Ui): alarmCheck 함수 실행')
        result_list = tests.limitLists(self.tests_list)
        result_list.sort(key=lambda x: x['enddate'], reverse=True)
        for i in result_list:
            now = time.time()
            if i['enddate'] - now <= 0: continue
            elif i['enddate'] - now < 86400 and not self.tests_alarm[i['name']]['day']:
                alarm.alarm('Tomatoma가 알려드려요.', f'"{i['name']}({i['subject']})" (이)가 하루도 안 남았어요!', self.path)
                self.tests_alarm[i['name']]['day'] = True
            elif i['enddate'] - now < 3600 and not self.tests_alarm[i['name']]['hour']:
                alarm.alarm('Tomatoma가 알려드려요.', f'"{i['name']}({i['subject']})" (이)가 한 시간도 안 남았어요!!', self.path)
                self.tests_alarm[i['name']]['hour'] = True
            elif i['enddate'] - now < 1800 and not self.tests_alarm[i['name']]['half']:
                alarm.alarm('Tomatoma가 알려드려요.', f'"{i['name']}({i['subject']})" (이)가 30분도 안 남았어요!!!', self.path)
                self.tests_alarm[i['name']]['half'] = True
            elif i['enddate'] - now < 60 and not self.tests_alarm[i['name']]['min']:
                alarm.alarm('Tomatoma가 알려드려요.', f'"{i['name']}({i['subject']})" (이)가 1분도 안 남았어요!!!!', self.path)
                self.tests_alarm[i['name']]['min'] = True


# GPT 안 썻어요 진짜 (창 드래그 빼고)