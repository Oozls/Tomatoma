# -*- coding:utf-8 -*-
from winotify import Notification
import os

def alarm(rtitle, rmsg, path):
    # print("Tomatoma (alarm.py): Alarm 함수 실행")
    notice = Notification(app_id='Tomatoma!', title=rtitle, msg=rmsg, icon=os.path.join(path,r'resources\ui\tomato.png')) # thread 안 됐으면 multi threading 가져오고 난리 났겠다
    notice.show()

# 솔직히 따로 ui에서 빼서 쓸 이유가 없긴 한데