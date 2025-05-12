# -*- coding:utf-8 -*-
# 수행평가 추가 및 수정, 삭제 등 역할 맡음, 데이터는 .json 파일로 저장

from collections import OrderedDict
import os, json

class Tests():
    def __init__(self):
        print("Tomatoma: tests.py -> Tests 클래스 Init")
    
    def add(self, path, name, desc, startdate, enddate, subject): # 수행평가 추가
        # path는 수행평가 데이터 저장하는 폴더

        print("Tomatoma(tests.py->Tests): add 함수 실행")
        print(f"Tomatoma(tests.py->Tests): path:{path}")

        data = OrderedDict()
        data['name'] = name
        data['desc'] = desc
        data['startdate'] = startdate
        data['enddate'] = enddate
        data['subject'] = subject

        with open(os.path.join(path,f'{name}.json'), 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent="\t")