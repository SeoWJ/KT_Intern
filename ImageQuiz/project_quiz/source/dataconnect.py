## (1) 컴퓨터 폴더로부터 이미지 data 불러오기 & 조회 연결 (현경 추가)
import os

# file_path = 'C:\\Users\82104\Desktop\celeb' ## 절대 경로 입력 (로컬 컴퓨터)
file_path = 'images'
file_names = os.listdir(file_path)
#print(file_names) ## ['강혜연.jpg', '거미.jpg', '고민시.jpg', '고소영.jpg', ..., '호날두.jpg']
#print(len(file_names)) ## 150

answerList = [] ## 인물 이름 리스트 (원종님 코드 ~ 추후 정답 처리 코드에서 엑셀파일 이름 리스트 대신 사용 가능하진 않을까요?)
person = {} ## 일련번호 및 인물 딕셔너리 (재현님 코드에서 person 변수로 활용하도록)

for idx, name in enumerate(file_names):
    #print(idx, name)
    person.setdefault(idx, name[:-4])
    answerList.append(name[:-4]) ## 추후 정답 처리 코드 등에서 같은 index 넘버로 NameData_list[key] => value 조회 가능
print(person) ## {0: '강혜연', 1: '거미', 2: '고민시', 3: '고소영', ..., 149: '호날두'}
print(NameData_list) ## ['강혜연', '거미', '고민시', '고소영', ..., '호날두']



'''
## (2) 점차 통과를 잘 안 주는(=난이도 증가) 단계별 퀘스트 알고리즘 아이디어 기록
def CLEAR_METHOD(step, answerList(?), person(?), 기타):
    print(str(step)+" 단계 - "+ str(step*2) + "문제 연속으로 맞추기 도전 !")

    ## WHILE 문으로 (??)
    while(True):
        res = 정답처리_METHOD()
        # IF (1) 모든 문제 다 맞췄다면
        if res == True:
            print(str(step) + ' 단계 CLEAR !')
            break
        # ELSE (2) 중간에 틀렸다면
        else:
            # 해당 step 값으로 다시 수행 ?
            print(str(step)+" 단계 - "+ str(step*2) + "문제 연속으로 맞추기 재도전 !")
            continue

step = 0
while(True):
    step += 1
    ## (Maximum 퀘스트 단계 내 수행)
    if step > 20:
        break

    ## 정답 카운트 메서드 결과 값에 따라 (리턴값)
    CLEAR_METHOD(입력값) # <- 입력값에는 step 변수가 들어가서 이를 활용해 점차 더 많은 문제를 맞춰야 퀘스트 클리어 완료를 인정하도록 수식에 활용
                            # (ex. step*2 개를 모두 연속하여 맞추어야 해당 단계 클리어 -2개, 4개, 6개, ...)
'''



