# # -*- coding:utf-8 -*-
# from jamo import h2j, j2hcj
# import difflib, os

# def search(answer_string, tests_list):
#     print(f'Tomatoma (search.py): search 함수 실행')

#     MoreThan50 = []

#     for i in tests_list:
#         answer_korean = j2hcj(h2j(answer_string.replace(' ', '').replace('수행', ''))) #입력값 자모로 변환
#         input_string = i['name'] #리스트 요소 훑기
#         input_korean = j2hcj(h2j(input_string.replace(' ', '').replace('수행',''))) #리스트 요소 자모로 변환
#         sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 자모 유사도 비교
#         similarity1 = int(sm.ratio() * 100)


#         answer_korean = list(answer_string.replace(' ', '').replace('수행','')) #입력값 글자 단위로 변환
#         input_korean = list((input_string.replace(' ', '').replace('수행',''))) #리스트 요소 글자 단위로 변환
#         sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 글자 유사도 비교
#         similarity2 = int(sm.ratio() * 100)

#         answer_korean = list(answer_string.replace('수행','').split()) #입력값 단어 단위로 변환
#         input_korean = list(input_string.replace('수행', '').split()) #리스트 요소 단어 단위로 변환
#         sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 단어 유사도 비교
#         similarity3 = int(sm.ratio() * 100)

#         similarity = int((similarity1 + similarity2 + similarity3) / 3)

#         if similarity >= 50:
#             MoreThan50.append(i)
        
#     if len(MoreThan50) == 0:
#         print(f'Tomatoma (search.py): 검색 결과 없음')
#     return MoreThan50

# # MADE BY ㄷㅈ

# -*- coding:utf-8 -*-
import hgtk
import difflib

def search(answer_string, tests_list):
    print(f'Tomatoma (search.py): search 함수 실행')

    result_list = []

    for i in tests_list: #input이 수행 목록
        cleaned_answer = answer_string.replace(' ', '').replace('수행', '')
        cleaned_input = i['name'].replace(' ', '').replace('수행', '')


        # -------- 음소 단위 유사도 검사 -------- #
        try:
            answer_jamo = hgtk.text.decompose(cleaned_answer)
            input_jamo = hgtk.text.decompose(cleaned_input)
        except hgtk.exception.NotHangulException:
            answer_jamo = cleaned_answer
            input_jamo = cleaned_input

        sm = difflib.SequenceMatcher(None, answer_jamo, input_jamo)
        similarity1 = int(sm.ratio() * 100)

        # 글자 단위 비교
        answer_chars = list(cleaned_answer)
        input_chars = list(cleaned_input)
        sm = difflib.SequenceMatcher(None, answer_chars, input_chars)
        similarity2 = int(sm.ratio() * 100)

        # 단어 단위 비교 ('수행' 제거 후 split)
        answer_words = list(answer_string.replace('수행', '').split())
        input_words = list(i['name'].replace('수행', '').split())
        sm = difflib.SequenceMatcher(None, answer_words, input_words)
        similarity3 = int(sm.ratio() * 100)

        similarity = int((similarity1 + similarity2 + similarity3) / 3)


        # -------- 앞 글자 일치 검사 -------- #
        input_substring = cleaned_input[:len(cleaned_answer)]

        if similarity >= 50 or cleaned_answer == input_substring:
            result_list.append(i)

    if len(result_list) == 0:
        print(f'Tomatoma (search.py): 검색 결과 없음')

    return result_list
# jamo 라이브러리 버그 때문에 hgtk 라이브러리로 대체한 버전