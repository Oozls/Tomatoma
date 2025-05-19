from jamo import h2j, j2hcj, j2h
import difflib

answer_string = input("검색 :")

sample_list = ["문학 소설 수행", "생명 2차 발표 수행", "일본어 말하기 수행"]

MoreThan50 = []

for i in range(len(sample_list)):
    answer_korean = j2hcj(h2j(answer_string.replace(' ', '').replace('수행', ''))) #입력값 자모로 변환환
    input_string = sample_list[i] #리스트 요소 훑기
    input_korean = j2hcj(h2j(input_string.replace(' ', '').replace('수행',''))) #리스트 요소 자모로 변환
    sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 자모 유사도 비교
    similarity1 = int(sm.ratio() * 100)


    answer_korean = list(answer_string.replace(' ', '').replace('수행','')) #입력값 글자 단위로 변환환
    input_korean = list((input_string.replace(' ', '').replace('수행',''))) #리스트 요소 글자 단위로 변환
    sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 글자 유사도 비교
    similarity2 = int(sm.ratio() * 100)

    answer_korean = list(answer_string.replace('수행','').split()) #입력값 단어 단위로 변환
    input_korean = list(input_string.replace('수행', '').split()) #리스트 요소 단어 단위로 변환
    sm = difflib.SequenceMatcher(None, answer_korean, input_korean) #입력값과 단어 유사도 비교
    similarity3 = int(sm.ratio() * 100)

    similarity = int((similarity1 + similarity2 + similarity3) / 3)

    if similarity >= 50:
        print(input_string, similarity,"%")
        MoreThan50.append(input_string)
    
if len(MoreThan50) == 0:
    print("검색 결과가 존재하지 않습니다.")

#print(MoreThan50)