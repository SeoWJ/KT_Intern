import os
import random
import threading
import time

import cv2
from PIL import Image

import ex1_kwstest_modified as kws
import ex2_getVoice2Text as tts
import sound
import os


# 한글 -> 로마자 변환 추가
# 예시: "배수지"를 넣으면 -> ['Bae Sooji', 'Bae Suji', 'Bae Soojee', 'Bae Sujee'] 결과가 생성됩니다.
# 레퍼런스: https://www.kimsungyoo.com/python-korean-name-to-english/
import urllib
from urllib import parse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

import googletrans # 영어 -> 한글 발음 변환 추가
from googletrans import Translator
translator = Translator()
##result = translator.translate("drake", src='en', dest="ko")
##print(result.text)

global answerList
global timerExitFlag

timerTimeSizeDefault = 10
countTrue = 0
countFalse = 0
combo = 0
score = 0

semaphore = threading.Semaphore(1)


def readData():
    file_path = 'images'
    file_names = os.listdir(file_path)

    answerList = list()

    for idx, name in enumerate(file_names):
        if (name[-3] + name[-2] + name[-1]) == 'jpg' or (name[-3] + name[-2] + name[-1]) == 'png':
            answerList.append(name[:-4])
        else:
            answerList.append(name[:-5])
            
    return answerList

def makeQuiz(answerList):
    answerListSize = len(answerList)
    answerIndex = random.randrange(answerListSize)

    answer = answerList[answerIndex]
    image = ""

    if os.path.isfile("images/" + answer + ".jpg"):
        image = "images/" + answer + ".jpg"
    elif os.path.isfile("images/" + answer + ".png"):
        image = "images/" + answer + ".png"
    elif os.path.isfile("images/" + answer + ".jfif"):
        image = "images/" + answer + ".jfif"
    elif os.path.isfile("images/" + answer + ".jpeg"):
        image = "images/" + answer + ".jpeg"

    del answerList[answerIndex]

    print("Answer : " + answer)
    print("Remain Question Amount : " + str(len(answerList)))

    return [answer, image]


def timerThread():
    global timerExitFlag
    remainTime = timerTimeSizeDefault
    # remainTime = 3.0 # 테스트용. 실제에서는 윗줄 사용.

    while (remainTime > 0 and timerExitFlag == 0):
        print(remainTime)
        time.sleep(1)
        remainTime = remainTime - 1

    semaphore.acquire()
    timerExitFlag = 1
    semaphore.release()


def quizStart(answer):
    global timerExitFlag, countTrue, countFalse, combo, score

    timerExitFlag = 0

    threadTimer = threading.Thread(target=timerThread)
    threadTimer.setDaemon(True)
    threadTimer.start()

    answerPossible = [answer]
    
    while 1:
        correct = False
        
        recog = kws.btn_test('기가지니')

        semaphore.acquire()
        if timerExitFlag == 1:
            semaphore.release()
            break
        semaphore.release()

        if recog == 200:
            print('KWS Dectected ...\n Start STT...')
            break

    # 음성 인식.
    stt = tts.getVoice2Text()
    print(stt)



    # STT 오류 해결을 위한 전처리 추가
    # 가능한 정답의 경우의 수를 증가시키는 컨셉입니다.
    answerPossible = [answer]  # (1)answer는 한글

    result = translator.translate(answer, src='ko', dest="en")
    res = result.text.replace(' ', '')
    answerPossible.append(res.lower())  # (2)정답의 영어발음은 기본으로 포함 시켰습니다. (소문자 설정 필수 !)


    # (3)한글 -> 로마자 변환을 통한 영어 발음을 추가했습니다.
    naver_url = 'https://dict.naver.com/name-to-roman/translation/?query='
    name_url = naver_url + urllib.parse.quote(answer)

    req = Request(name_url)
    res = urlopen(req)

    html = res.read().decode('utf-8')
    bs = BeautifulSoup(html, 'html.parser')
    name_tags = bs.select('#container > div > table > tbody > tr > td > a')
    names = [name_tag.text for name_tag in name_tags]
    names_low = [elem.lower().replace(' ', '') for elem in
                         names]  # 혹시 몰라서 소문자 변환 추가하였고, stt 변수와 동일하게 공백을 제거해주어습니다.
    ##stt = stt.lower() # stt 변수도 소문자 변환 동일하게 적용했습니다.
    #print(names)
    #print(names_low)

    answerPossible.extend(names_low)
    # print(answerPossible)

    # (4)구글 번역 결과 확장하여 다양한 영어이름의 한국어 발음도 추가했습니다.


    # (5) 영어를 한글 표기법 발음으로 변환해주는 사이트도 추가하고 싶습니다. (https://transliterator.herokuapp.com/)


    #print(answerPossible)




    #if any(chr.isalpha() == True for chr in stt) == True:  # STT 결과에 한글자라도 영어 포함되어 있으면
    stt = stt.lower()  # stt 변수도 소문자 변환 동일하게 적용했습니다.
    #####res = translator.translate(stt, src='en', dest="ko")
    # print(res.text)
    #####stt = res.text


    # 정답 확인.
    # if stt.find(answer) >= 0:
    if any(stt.find(ans) >= 0 for ans in answerPossible) == True:  # 가능한 정답 리스트(answerPossible) 중 STT 내 정답이 포함된 경우가 하나라도 있는지 판별합니다.

        sound.correctSound()

        countTrue += 1
        combo += 1
        score += 10 * combo
        correct = True


        print("\nCorrect.\n")


    else:
        sound.wrongSound()

        countFalse += 1
        combo = 0
        correct = False
                
        print("\nWrong.\n")

    print("정답 갯수: " + str(countTrue))
    print("오답 갯수: " + str(countFalse))
    print("점수:  " + str(score) + '점')

    semaphore.acquire()
    timerExitFlag = 1
    semaphore.release()

    return correct
