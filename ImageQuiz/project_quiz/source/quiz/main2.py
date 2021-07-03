import sys
import urllib.request
from PyQt5 import QtCore,QtWidgets,uic,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt,QPoint,QRectF
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QProcess,QTimer

import time
import random
import ex1_kwstest2 as kws
import ex2_getVoice2Text2 as tts
#import ex6_queryVoice as dss
import MicrophoneStream as MS
import threading
import csv
import os
import cv2
import sound
from PIL import Image


person={0:'신서유기', 1:'유재석',2:'음료수',3:'강호동',4:'규현',5:'바이든',6:'송민호',7:'안재현',8:'은지원',9:'이수근',10:'카리나',11:'피오'}

form_class = uic.loadUiType("intro.ui")[0]
form_class2 = uic.loadUiType("end.ui")[0]


timerTimeSizeDefault = 10	#문제당 시간 
questionNum = 10	#출제 문제 갯수
global answerList
global timerExitFlag
global randList, gg
countTrue = 0
countFalse = 0
semaphore = threading.Semaphore(1)

gg=0
combo = 0
score = 0


class MySignal(QObject):
    signal1 = pyqtSignal()
    signal2 = pyqtSignal(int, int)


        

class Intro(QMainWindow, form_class):
    global questionNum, countTrue, countFalse, score, randList, answerList
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.keyPressEvent2()
        
        #mysignal = MySignal()
        #mysignal.signal1.connect(self.signal1_emitted)
        #mysignal.signal2.connect(self.signal2_emitted)
        #mysignal.run()
        self.timer = QtCore.QTimer(self)
        self.timer.start(100)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.keyPressEvent2)
        #self.timer.singleShot(10, self.keyPressEvent2)
        
        
        
    #def mousePressEvent(self, event):
    #    self.c.closeApp.emit()
    
    
    def keyPressEvent2(self):
        #입력 상황
        #print(1)
        global questionNum, countTrue, countFalse, score, randList, answerList
        recog = kws.btn_test('기가지니')
        
        if recog == 200 and widget.currentIndex()==0:
            
            readData()
            randList = random_List(questionNum, len(answerList))
            print(randList)
            widget.setCurrentIndex(widget.currentIndex()+1)
            widget.setStyleSheet(
                "background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")
            print(widget.currentIndex())
            self.timer.stop()
        #print(1000)

class End(QMainWindow, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_A:
            widget.setCurrentIndex(widget.currentIndex()==0)
            print(widget.currentIndex())

class UIApp(QWidget):
    global questionNum, countTrue, countFalse, score,randList, answerList, person, gg
    key = 0
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer2 = QtCore.QTimer(self)
        self.timer2.start(100)
        self.timer2.setInterval(10)
        self.timer2.timeout.connect(self.keyPressEvent2)


    def initUI(self):

        '''★★★★★★★여기 추가 됐어요!!!!!!★★★★★★★★★★★'''
        #self.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")

        #이미지 오브젝트 받아옴 (딕셔너리 형태) 초기값은 신서유기8 페이지
        self.key=0
        pic=person[self.key]

        #이미지 오브젝트 -> 이미지 라벨로 픽셀 표시
        self.obj = QPixmap(pic)
        self.obj= self.obj.scaledToHeight(800)
        self.img_label = QLabel()
        self.img_label.setPixmap(self.obj)
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setStyleSheet("background-color : transparent")

        #file name(image name)
        self.img_name=QLabel()
        self.img_name.setText(pic)
        self.img_name.setFont(QFont("궁서", 50))  # 폰트,크기 조절
        self.img_name.setStyleSheet("Color : red")
        self.img_name.setAlignment(Qt.AlignCenter)


        '''★★★★★★★여기 추가 됐어요!!!!!!★★★★★★★★★★★'''
        #카운트 UI
        self.lcd = QLCDNumber()
        self.lcd.display(self.key)
        self.lcd.setDigitCount(1)
        self.lcd.setFixedWidth(200)
        self.lcd.setFixedHeight(100)
        self.lcd.setStyleSheet("""QLCDNumber {background-color: red;}""")

        '''★★★★★★★여기 교체해주세요!!!!!!★★★★★★★★★★★'''
        #UI layout
        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(self.img_label)
        hbox.addStretch(1)
        hbox.addWidget(self.lcd, 0, Qt.AlignTop)
        #vbox.addWidget(self.img_name)

        self.setLayout(hbox)

        self.setWindowTitle('나영석PD')
        self.move(400,50)

        #self.show()
        self.showMaximized()

    #입력 event 처리
    def keyPressEvent2(self):
        #입력 상황
        global gg
        recog = kws.btn_test('기가지니')
        
        if recog == 200 and widget.currentIndex()==1:
            while 1:
                if tts.getVoice2Text().find(person[self.key])>=0:
                    break
            #self.key=random.randint(1,len(person.keys())-1)
            self.key+=1
            pic = person[self.key]
            self.obj = QPixmap(pic)
            self.obj = self.obj.scaledToHeight(800)
            self.img_label.setPixmap(self.obj)
            self.lcd.display(self.key)
            print(self.key)
            gg+=1

            #이미지 명
            self.img_name.setText(pic)
            
            #while 1:			
            #    time.sleep(1)								#호출어(기가지니)로 프로그램 실행 
            #if tts.getVoice2Text().find("인물퀴즈")>=0:
            
            """
            count = questionNum

            while count > 0:
	
                makeQuiz()
                count-=1

            print("정답 갯수: " + str(countTrue))
            print("오답 갯수: " + str(countFalse))
            print("정답률: " + str(countTrue/questionNum*100) +  '%')
            print("점수:  " +str(score) + '점')
            del answerList
            """
        #실패입력
       # if e.key() == Qt.Key_A:
       #     widget.setCurrentIndex(widget.currentIndex() + 1)
       #     print(widget.currentIndex())
        #종료상황
            #if e.key()== Qt.Key_Backspace:
            #    self.close()


def readData():
	global answerList
	
	file_path = 'images'
	file_names = os.listdir(file_path)
	
	answerList = list()
	person = {}

	for idx, name in enumerate(file_names):
		if (name[-3] + name[-2] + name[-1]) == 'jpg' or (name[-3] + name[-2] + name[-1]) == 'png':
			person.setdefault(idx, name[:-4])
			answerList.append(name[:-4])
		else:
			person.setdefault(idx, name[:-5])
			answerList.append(name[:-5])
			
	# Old Version.
	"""global answerList
	
	answerList = list()
	
	f = open("data/NameData.csv", 'r', encoding = 'utf-8-sig')
	fd = csv.reader(f)
	
	for line in fd:
		answerList.append(line[0])
		
	f.close()"""
	
	
def random_List(imageNum, maxImageNum):
	result = []
	
	for v in range(maxImageNum):
		
		result.append(v)
		random.shuffle(result)
		
	return result[0:imageNum]
	


def makeQuiz():
	
	global answerList, randList
	answerIndex = randList.pop(0)
		
	answer = answerList[answerIndex]
	quizImage = 0
	
	if os.path.isfile("images/" + answer + ".jpg"):
		quizImage = Image.open("images/" + answer + ".jpg")
	elif os.path.isfile("images/" + answer + ".png"):
		quizImage = Image.open("images/" + answer + ".png")
	elif os.path.isfile("images/" + answer + ".jfif"):
		quizImage = Image.open("images/" + answer + ".jfif")
	elif os.path.isfile("images/" + answer + ".jpeg"):
		quizImage = Image.open("images/" + answer + ".jpeg")
	#quizImage.save(answer+"png")
	print("Answer : " + answer)
	print("Remain Question Amount : " + str(len(answerList)))
	
	if not quizImage == 0:
		quizStart(answer, quizImage)
	else:
		return 1
		
def timerThread():
	global timerExitFlag
	remainTime = timerTimeSizeDefault
	# remainTime = 3.0 # 테스트용. 실제에서는 윗줄 사용.
	
	while(remainTime > 0 and timerExitFlag == 0):
		print(remainTime)
		time.sleep(1)
		remainTime = remainTime - 1
	
	semaphore.acquire()	
	timerExitFlag = 1
	semaphore.release()
		
		
def quizStart(answer, quizImage):
	global timerExitFlag, countTrue, countFalse, combo, score
	
	timerExitFlag = 0
	
	threadTimer= threading.Thread(target = timerThread)
	threadTimer.setDaemon(True)
	threadTimer.start()	
		
	while 1:
		recog = kws.btn_test('기가지니')
		
		semaphore.acquire()
		if timerExitFlag == 1:
			semaphore.release()
			break
		semaphore.release()
		
		
		if recog == 200:
			print('KWS Dectected ...\n Start STT...')
			
			# 음성 인식.
			stt = tts.getVoice2Text()
			#print(stt)
		
			# 정답 확인.
			if stt.find(answer.replace(" ","")) >= 0:
				sound.correctSound()
				countTrue += 1
				combo += 1
				score += 10*combo
				print("Correct.")
			else:
				#wrong_image = cv2.imread('audios/wrong_image.jpg')
				sound.wrongSound()
				countFalse += 1
				combo = 0
				#cv2.imshow('Wrong', wrong_image)
				#cv2.waitKey(1000)
				print("Wrong")
				#cv2.destroyAllWindows()
				
			print("정답 갯수: " + str(countTrue))
			print("오답 갯수: " + str(countFalse))
			print("정답률: " + str(countTrue/questionNum*100) +  '%')
			print("점수:  " +str(score) + '점')
			
			semaphore.acquire()	
			timerExitFlag = 1
			semaphore.release()
			
	time.sleep(3)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()
    """
    while 1:			
        time.sleep(0.2)								#호출어(기가지니)로 프로그램 실행 
        if tts.getVoice2Text().find("기가지니")>=0:
            break
    """
    # 레이아웃 인스턴스 생성
    Window1 = Intro()
    Window2 = UIApp()
    Window3 = End()

    # Widget 추가
    widget.addWidget(Window1)
    widget.addWidget(Window2)
    widget.addWidget(Window3)

    # 프로그램 화면을 보여주는 코드
    widget.showMaximized()
    print(widget.currentIndex())

    sys.exit(app.exec_())
