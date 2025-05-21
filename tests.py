# -*- coding:utf-8 -*-
# 수행평가 추가 및 수정, 삭제 등 역할 맡음, 데이터는 .json 파일로 저장

from collections import OrderedDict
import os, json

def add(path, name, desc, enddate, subject): # 수행평가 추가
    # path는 수행평가 데이터 저장하는 폴더
    if not os.path.exists(path): os.mkdir(path)

    print("Tomatoma (tests.py): add 함수 실행")
    print(f"Tomatoma (tests.py): path={path}")

    data = OrderedDict()
    data['name'] = name
    data['desc'] = desc
    data['enddate'] = enddate
    data['subject'] = subject

    with open(os.path.join(path,f'{name}.json'), 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent="\t")

def lists(path):
    if not os.path.exists(path): os.mkdir(path)

    print("Tomatoma (tests.py): lists 함수 실행")
    print(f"Tomatoma (tests.py): path={path}")

    json_data_list = []

    # 폴더 내 파일들 순회
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            file_path = os.path.join(path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    json_data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Tomatoma (tests.py): JSON 오류: {filename} - {e}")
            except Exception as e:
                print(f"Tomatoma (tests.py): 파일 읽기 오류: {filename} - {e}")
    
    print(f"Tomatoma (tests.py): json_data_list={json_data_list}")

    return json_data_list