from jamo import h2j, j2hcj
import difflib, os

def search(answer_string, tests_list):
    print(f'Tomatoma (search.py): search 함수 실행')

    MoreThan50 = []

    for i in tests_list:
        answer_korean = j2hcj(h2j(answer_string.replace(' ', '').replace('수행', ''))) #입력값 자모로 변환
        input_string = i['name'] #리스트 요소 훑기
        input_korean = j2hcj(h2j(input_string.replace(' ', '').replace('수행',''))) #리스트 요소 자모로 변환
        sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 자모 유사도 비교
        similarity1 = int(sm.ratio() * 100)


        answer_korean = list(answer_string.replace(' ', '').replace('수행','')) #입력값 글자 단위로 변환
        input_korean = list((input_string.replace(' ', '').replace('수행',''))) #리스트 요소 글자 단위로 변환
        sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 글자 유사도 비교
        similarity2 = int(sm.ratio() * 100)

        answer_korean = list(answer_string.replace('수행','').split()) #입력값 단어 단위로 변환
        input_korean = list(input_string.replace('수행', '').split()) #리스트 요소 단어 단위로 변환
        sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 단어 유사도 비교
        similarity3 = int(sm.ratio() * 100)

        similarity = int((similarity1 + similarity2 + similarity3) / 3)

        if similarity >= 50:
            MoreThan50.append(i)
        
    if len(MoreThan50) == 0:
        print(f'Tomatoma (search.py): 검색 결과 없음')
    return MoreThan50

# MADE BY ㄷㅈ