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
import ex1_kwstest_modified as kws
import ex2_getVoice2Text as tts
import MicrophoneStream as MS
import csv
import os
import sound
from PIL import Image

form_class = uic.loadUiType("intro.ui")[0]
form_class2 = uic.loadUiType("end.ui")[0]


timerTimeSizeDefault = 10	#문제당 시간 
questionNum = 10	#출제 문제 갯수
global timerExitFlag
global gg
countTrue = 0
countFalse = 0

imageList=[]
randList=[]
answerList=[]



class Intro(QMainWindow, form_class):
	global questionNum, countTrue, countFalse, score, randList, answerList, imageList
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.timer = QtCore.QTimer(self)
		self.timer.start(100)
		self.timer.setInterval(10)
		self.timer.timeout.connect(self.keyPressEvent2)
    
    
	def keyPressEvent2(self):
		#입력 상황
		global questionNum, countTrue, countFalse, score, answerList, imageList
		recog = kws.btn_test('기가지니')
		
		if recog == 200 and widget.currentIndex()==0:
            
			answerList=self.readData()
			
			randList=self.random_List(questionNum,len(answerList))
			imageList, answerList =self.makeQuiz(randList)
			
			print(answerList)
			print(imageList)
			widget.setCurrentIndex(widget.currentIndex()+1)
			widget.setStyleSheet(
				"background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")
			print(widget.currentIndex())
			self.timer.stop()
	
	def readData(self):
		global answerList
	
		file_path = 'images'
		file_names = os.listdir(file_path)
	
		answerList = list()
		per = {}
	
		for idx, name in enumerate(file_names):
			if (name[-3] + name[-2] + name[-1]) == 'jpg' or (name[-3] + name[-2] + name[-1]) == 'png':
				per.setdefault(idx, name[:-4])
				answerList.append(name[:-4])
			else:
				per.setdefault(idx, name[:-5])
				answerList.append(name[:-5])
		#print(answerList)
		return answerList	
	
	def random_List(self,imageNum, maxImageNum):
		result = []
	
		for v in range(maxImageNum):
		
			result.append(v)
			random.shuffle(result)
		return result[0:imageNum]

	def makeQuiz(self, randList):
	
		global answerList
		answerSortedList=[]

		while len(randList)>0:
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
			imageList.append(quizImage)
			answerSortedList.append(answer)

		#quizImage.save(answer+"png")
		return imageList, answerSortedList

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
	global questionNum, countTrue, countFalse, score, randList, answerList, person, imageList
	key = 0
	quizStart = 0	#퀴즈화면으
	timeCount = 10

	def __init__(self):
		super().__init__()
		self.initUI()
		self.timer2 = QtCore.QTimer(self)
		self.timer2.start(1000)
		self.timer2.setInterval(200)
		self.timer2.timeout.connect(self.buttonClicked)
		
		self.timer3 = QtCore.QTimer(self)
		self.timer3.start(0)
		self.timer3.setInterval(1000)
		self.timer3.timeout.connect(self.timeCounter)
		
		

	def initUI(self):

		'''★★★★★★★여기 추가 됐어요!!!!!!★★★★★★★★★★★'''
		#self.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")

		#이미지 오브젝트 받아옴 (딕셔너리 형태) 초기값은 신서유기8 페이지
		self.key=0
		pic="신서유기"

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
		self.lcd.display(self.timeCount)
		self.lcd.setDigitCount(1)
		self.lcd.setFixedWidth(200)
		self.lcd.setFixedHeight(100)
		self.lcd.setStyleSheet("""QLCDNumber {background-color: red;}""")
		
		#정답 갯수
		self.lcd2 = QLCDNumber()
		self.lcd2.display(self.key)
		self.lcd2.setDigitCount(1)
		self.lcd2.setFixedWidth(200)
		self.lcd2.setFixedHeight(100)
		self.lcd2.setStyleSheet("""QLCDNumber {background-color: blue;}""")

		'''★★★★★★★여기 교체해주세요!!!!!!★★★★★★★★★★★'''
		#UI layout
		hbox = QHBoxLayout()
		hbox.addStretch(2)
		hbox.addWidget(self.img_label)
		hbox.addStretch(1)
		hbox.addWidget(self.lcd, 0, Qt.AlignTop)
		hbox.addWidget(self.lcd2, 0, Qt.AlignTop)
		#vbox.addWidget(self.img_name)

		self.setLayout(hbox)

		self.setWindowTitle('나영석PD')
		self.move(400,50)

		#self.show()
		self.showMaximized()

	#입력 event 처리
	def buttonClicked(self):

		recog = kws.btn_test('기가지니')		#버튼 입력
		
		if (recog == 200 and widget.currentIndex()==1 and self.quizStart != 0): #버튼입력 and 2번째 UI and 퀴즈 준비화면 상태 
			
			#print(answerList) 
			#print(imageList)
			
			print(recog)
			answerCount=1
			ttsList=[]
			
			#음성입력
			while answerCount>0:
				ttsList.append(tts.getVoice2Text().find(answerList[self.key]))
				answerCount-=1
				
			if sum(ttsList)!=(-1)*len(ttsList):	#정답
				
				sound.correctSound()
				self.timeCount = 10
				self.key+=1
				pic = answerList[self.key]
				self.obj = QPixmap(pic)
				self.obj = self.obj.scaledToHeight(500)
				self.lcd.display(self.timeCount)	
				self.lcd2.display(self.key)		#정답갯수 표시
				self.img_label.setPixmap(self.obj)
				
				#이미지 명
				self.img_name.setText(pic)
				
			else:				#오답
				widget.setCurrentIndex(widget.currentIndex() + 1)
				sound.wrongSound()
				self.timer2.stop()
				self.timer3.stop()
			
		elif recog == 200 and self.quizStart==0:	#준비화면에서 문제출제화면으로 전환
			pic = answerList[self.key]
			self.obj = QPixmap(pic)
			self.obj = self.obj.scaledToHeight(500)
			self.img_label.setPixmap(self.obj)
			self.lcd.display(self.timeCount)
			print(self.key)
			self.quizStart += 1

			#이미지 명
			self.img_name.setText(pic)
			self.timeCount = 10

	def timeCounter(self):	#타이머

		if self.timeCount > 0 and self.quizStart != 0:		#타이머 및 실시간 시간표시
			self.timeCount-=1
			self.lcd.display(self.timeCount)
			print(self.timeCount)
			
		elif self.timeCount ==0 and self.gg != 0:	#타이머 종료 "끝" 화면으로 전환
			widget.setCurrentIndex(widget.currentIndex() + 1)
			sound.wrongSound()
			self.timer2.stop()
			self.timer3.stop()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	# 화면 전환용 Widget 설정
	widget = QtWidgets.QStackedWidget()
	
	#while 1:			      								#호출어(기가지니)로 프로그램 실행 
	#	if tts.getVoice2Text().find("기가지니")>=0:
	#		break
	#	time.sleep(1)
			
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
