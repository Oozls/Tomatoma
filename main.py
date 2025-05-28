# -*- coding:utf-8 -*-
# 이름 그대로 총괄적인 역할



# 라이브러리
from PyQt5 import QtWidgets
import sys, os
import icons


from ui import Ui



# 나중에 pyinstaller로 .exe로 변환해서 실행하면 경로가 다르게 설정되는 거 보정해주는 코드 / 걍 무시하자
# 파일 경로 같은건 다 main.py에서 다룰 거임 <- 안 하면 밑에 있는 코드 다 .py 파일들 위에 넣어야 함
import sys
if getattr(sys, 'frozen', False):
    #test.exe로 실행한 경우,test.exe를 보관한 디렉토리의 full path를 취득
    current_path = os.path.dirname(os.path.abspath(sys.executable))
else:
    #python test.py로 실행한 경우,test.py를 보관한 디렉토리의 full path를 취득
    current_path = os.path.dirname(os.path.abspath(__file__))



# 이 프로그램이 메인으로 실행되었을 때
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) #뭔지 모름
    window = Ui(current_path) # ui.py 파일에 있는 클래스 Ui 실행
    app.exec_()

    # 여기 뒤로는 Ui 닫아야 실행됨.

    # print("Tomatoma: Ui 닫힘")