import sys

#pyqt UI 사용을 위한 라이브러리
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt,QPoint,QRectF
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QProcess, QRunnable, QThreadPool, QTimer, QTime


import time
import random

#참조 파이썬 파일
import ex1_kwstest2 as kws
import ex2_getVoice2Text2 as tts
import MicrophoneStream as MS

import urllib.request
import os
import sound
from PIL import Image, ImageOps
import requests
import subprocess

from io import StringIO
import tensorflow.keras
import numpy as np

form_class0 = uic.loadUiType("gamemenu.ui")[0]
form_class1 = uic.loadUiType("intro.ui")[0]
form_class2 = uic.loadUiType("miss.ui")[0]


timerTimeSizeDefault = 10	#문제당 시간 
questionNum = 5	#출제 문제 갯수
global timerExitFlag

countTrue = 0
countFalse = 0

#게임 재시작을 위한 변수
regame = 1
finish = 0

imageList=[]
randList=[]
answerList=[]


## Settings
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model(과일퀴즈)
model = tensorflow.keras.models.load_model('keras_model.h5')
# 포즈퀴즈 제시어 리스트
subjects = ["비상구", "자유의여신상", "축구선수"]
# 포즈퀴즈 정답 이미지
subjects_image=["/home/pi/Desktop/kt팀프로젝트/img/answer_exit.jpg","/home/pi/Desktop/kt팀프로젝트/img/answer_freewoman.jpg","/home/pi/Desktop/kt팀프로젝트/img/answer_soccer.jpg"]
# 과일퀴즈 리스트
ansDict = {0: '사과', 1: '바나나', 2: '포도', 3: '딸기', 4: '레몬', 5: 0} # 해당 퀴즈에서 과일의 종류는 다음과 같습니다.

quiz_num=1

class gameStart(QMainWindow, form_class0):
	
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setFocusPolicy(Qt.StrongFocus)
		
		
	def keyPressEvent(self, e):
		if widget.currentIndex()==0:
			
			if e.key() == Qt.Key_A:
				widget.setCurrentIndex(widget.currentIndex()+1)
				print("#########################")		
				
			elif e.key() == Qt.Key_B:
				print("222222222222222222")
				self.www = poseQuiz()
				self.www.show()
				
			elif e.key() == Qt.Key_C:
				print("333333333333")
								
				self.f1 = fruitQuiz()
				self.f2 = fruitQuiz3()
				self.f3 = fruitQuiz2()
				
				fwidget.addWidget(self.f1)
				fwidget.addWidget(self.f2)
				fwidget.addWidget(self.f3)
				fwidget.showMaximized()
				
			elif e.key() == Qt.Key_Space:
				print("222222222222222222")
				quit()


class Intro(QMainWindow, form_class1):
	
	global questionNum, countTrue, countFalse, score, randList, answerList, imageList
	buttonClicked= 0
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.timer = QtCore.QTimer(self)
		self.timer.setInterval(100)
		self.timer.timeout.connect(self.keyPressEvent2)
		self.timer.start(0)
		print("Intro")
    
    
	def keyPressEvent2(self):
		#입력 상황
		global questionNum, countTrue, countFalse, score, answerList, imageList
		#global Window2
		if self.buttonClicked == 0 and widget.currentIndex()==1:
			recog = kws.btn_test('기가지니')
			
			if recog == 200:
				self.buttonClicked = 1
				print("*************시작*****************")
				answerList=self.readData()
				print(len(answerList))
				randList=self.random_List(questionNum,len(answerList)-1)
				print(randList)
				imageList, answerList =self.makeQuiz(randList)
					
				print(answerList)

				widget.setCurrentIndex(widget.currentIndex()+1)
				widget.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")
				self.timer.stop()
				self.buttonClicked = 0

				
			
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
			answerSortedList.append(answer.replace(" ",""))
		print(answerSortedList)
		return imageList, answerSortedList


class End(QMainWindow, form_class2):
	global finish
	count = 50
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.timer4 = QtCore.QTimer(self)
		self.timer4.start(1000)
		self.timer4.setInterval(100)
		self.timer4.timeout.connect(self.restartGame)

	def restartGame(self):
		#입력 상황
		global regame
		if finish == 1 and widget.currentIndex()==3:
		
			
			recog = kws.btn_test('기가지니')		#버튼 입력
			if (recog == 200 and widget.currentIndex() == 3): #버튼입력 and "끝" 화면 상태 
				regame = 1
				self.timer4.stop()				
				self.close()
				app.quit()


class UIApp(QWidget):
	global questionNum, countTrue, countFalse, score, randList, answerList, person, imageList
	key = 0
	quizStart = 0	#퀴즈화면
	timeCount = 10
	stopbutton = 0
	def __init__(self):
		super().__init__()
		self.initUI()
		self.timer2 = QtCore.QTimer(self)
		self.timer2.start(1000)
		self.timer2.setInterval(10)
		self.timer2.timeout.connect(self.buttonClicked)
		
		self.timer3 = QtCore.QTimer(self)
		self.timer3.start(0)
		self.timer3.setInterval(1000)
		self.timer3.timeout.connect(self.timeCounter)
		
		

	def initUI(self):
		global questionNum
		#이미지 오브젝트 받아옴 (딕셔너리 형태) 초기값은 신서유기8 페이지
		self.key=0
		pic="신서유기"

		#이미지 오브젝트 -> 이미지 라벨로 픽셀 표시
		self.obj = QPixmap(pic)
		self.obj= self.obj.scaledToHeight(1000)
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

		#카운트 UI
		self.lcd = QLCDNumber()
		self.lcd.display(self.timeCount)
		self.lcd.setDigitCount(1)
		self.lcd.setFixedWidth(150)
		self.lcd.setFixedHeight(100)
		self.lcd.setStyleSheet("""QLCDNumber {background-color: red;}""")
		
		#정답 갯수
		self.lcd2 = QLCDNumber()
		self.lcd2.display(self.key)
		self.lcd2.setDigitCount(1)
		self.lcd2.setFixedWidth(150)
		self.lcd2.setFixedHeight(100)
		self.lcd2.setStyleSheet("""QLCDNumber {background-color: blue;}""")
		
		self.lcd3 = QLCDNumber()
		self.lcd3.display(questionNum / 5)
		self.lcd3.setDigitCount(1)
		self.lcd3.setFixedWidth(150)
		self.lcd3.setFixedHeight(100)
		self.lcd3.setStyleSheet("""QLCDNumber {background-color: green;}""")

		#UI layout
		hbox = QHBoxLayout()
		hbox.addStretch(2)
		hbox.addWidget(self.img_label)
		hbox.addStretch(1)
		hbox.addWidget(self.lcd, 0, Qt.AlignTop)
		hbox.addWidget(self.lcd2, 0, Qt.AlignTop)
		hbox.addWidget(self.lcd3, 0, Qt.AlignTop)
		
	
		self.label1 = QLabel(self)
		self.label1.setGeometry(1470, 110, 450, 22)
		self.label1.setText("     남은 시간                         정답 갯수                            레벨")

		self.setLayout(hbox)

		self.setWindowTitle('나영석PD')
		self.move(400,50)

		self.showMaximized()

	#입력 event 처리
	def buttonClicked(self):
		global finish, regame, questionNum
		if self.stopbutton == 0 and widget.currentIndex()==2:
			
			recog = kws.btn_test('기가지니')		#버튼 입력
			
			if (recog == 200 and widget.currentIndex() == 2 and self.quizStart != 0): #버튼입력 and 2번째 UI and 퀴즈 준비화면 상태 
				self.stopbutton = 1
				
				print(recog)
				answerCount=1
				ttsList=[]
				cancelList=[]
				#음성입력
				while answerCount>0:
					voice = tts.getVoice2Text()
					ttsList.append(voice.find(answerList[self.key].replace(" ","")))
					cancelList.append(voice.find("종료"))
					answerCount -= 1
					
				print(cancelList)
				
				if sum(ttsList) != (-1)*len(ttsList):	#정답
					
					sound.correctSound()
					self.timeCount = 10
					self.key += 1
					print(questionNum, self.key)
					if questionNum == self.key:
						questionNum += 5
						regame = 1
						app.quit()
					else:	
						pic = answerList[self.key]
						self.obj = QPixmap(pic)
						self.obj = self.obj.scaledToHeight(1000)
					
						self.img_label.setPixmap(self.obj)
						self.lcd.display(self.timeCount)	
						self.lcd2.display(self.key)		#정답갯수 표시
						
						#이미지 명
						self.img_name.setText(pic)
						self.stopbutton = 0
						
						
				elif sum(cancelList) != (-1)*len(cancelList):
					self.timer2.stop()
					self.timer3.stop()
					quit()
				else:				#오답
					widget.setCurrentIndex(widget.currentIndex() + 1)

					sound.wrongSound()
					finish = 1
					self.timer2.stop()
					self.timer3.stop()
					self.close()
				
			elif recog == 200 and self.quizStart == 0 and widget.currentIndex()==2:	#준비화면에서 문제출제화면으로 전환
				pic = answerList[self.key]
				self.obj = QPixmap(pic)
				self.obj = self.obj.scaledToHeight(1000)
				self.img_label.setPixmap(self.obj)
				self.lcd.display(self.timeCount)
				print(self.key)
				self.quizStart += 1

				#이미지 명
				self.img_name.setText(pic)
				self.timeCount = 10
				self.stopbutton = 0

	def timeCounter(self):	#타이머
		global finish
		if widget.currentIndex()==2:
			if self.timeCount > 0 and self.quizStart != 0:		#타이머 및 실시간 시간표시
				self.timeCount-=1
				self.lcd.display(self.timeCount)
				print(self.timeCount)
				
			elif self.timeCount ==0 and self.quizStart != 0:	#타이머 종료 "끝" 화면으로 전환
				widget.setCurrentIndex(widget.currentIndex() + 1)
				sound.wrongSound()
				finish = 1
				self.timer2.stop()
				self.timer3.stop()


#이미지 촬영
def takePicture():
	time.sleep(2)
	command = "raspistill -t 1 -o photo.jpg"   
	subprocess.call(command, shell = True)

#이미지 용량 축소
def resizeImg():
	file = 'photo.jpg'
	img = Image.open(file)
	img = img.resize((600, 800), Image.ANTIALIAS)
	img.save('photo.jpg', quality=50)

#포즈 유사도 계산 알고리즘
def cal_tan(pos1, pos2):
	if pos1[0] == pos2[0] :
		pos1[0] += 0.01
	return (pos1[1]-pos2[1])/(pos1[0]-pos2[0])

def cal_average(li):
	sum=0
	for i in li:
		sum += i
	return sum / (len(li))
#오차율 계산 함수
def cal_error(pivot, data, leng):
	err = 0
	for i in range (0,leng):
		err += pivot[i] - data[i]
	return err / leng

#포즈 분석 수행
def analyzePose(self):
	resizeImg() #용량 축소한 이미지 입력
	APP_KEY = 'cccb25671d4102f9c8fde1d68f529ce1'
	IMAGE_URL ='photo.jpg'
	IMAGE_FILE_PATH = 'photo.jpg'
	session = requests.Session()
	session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

	# URL로 이미지 입력시
	response = session.post('https://cv-api.kakaobrain.com/pose', data={'image_url': IMAGE_URL})

	#이미지 파일 불러오기
	with open(IMAGE_FILE_PATH, 'rb') as f:
		response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', f)])
		print('응답코드',response.status_code, response.json())
		
		flag=0
		if len(response.json())==0 or len(response.json())==1:
			print('다시 촬영하겠습니다')
			print(len(response.json()))
			flag=1
			return 1, 1, flag
			
		#player1, player2 포즈 좌표값 저장
		keypoints1=response.json()[0]['keypoints']
		keypoints2=response.json()[1]['keypoints']

        
		pose_data1=[]
		pose_data2=[]

		for i in range(0,len(keypoints1)-2,3):
			pose_data1.append([keypoints1[i],keypoints1[i+1]])
			pose_data2.append([keypoints2[i],keypoints2[i+1]])
        
		print(pose_data1, pose_data2)

	#정답 포즈 좌표값
	exit_pivot = [[299.5312, 123.7031], [311.5848, 122.4844], [289.8884, 110.2969], [317.6116, 140.7656], [273.0134, 117.6094], [307.9688, 268.7344], [221.183, 196.8281], [369.442, 361.3594], [151.2723, 235.8281], [392.3438, 235.8281], [131.9866, 363.7969], [275.4241, 516.1406], [222.3884, 522.2344], [280.2455, 659.9531], [216.3616, 661.1719], [205.5134, 773.2969], [207.9241, 773.2969]]
	freewoman_pivot=[[315.2009, 240.7031], [326.0491, 233.3906],[307.9688, 233.3906], [339.308, 254.1094], [300.7366, 244.3594], [361.0045, 333.3281], [280.2455, 318.7031], [375.4688, 430.8281], [242.8795, 256.5469], [340.5134, 407.6719], [219.9777, 178.5469], [328.4598, 521.0156], [291.0938, 516.1406], [330.8705, 651.4219], [281.4509, 645.3281], [332.0759, 764.7656], [277.8348, 755.0156]]
	soccer_pivot=[[303.1473, 167.5781], [311.5848, 160.2656], [293.5045, 155.3906], [316.4062, 170.0156], [277.8348, 160.2656], [306.7634, 262.6406], [248.9063, 218.7656], [348.9509, 306.5156], [206.7188, 297.9844], [401.9866, 336.9844], [182.6116, 373.5469], [260.9598, 419.8594], [245.2902, 411.3281], [271.808, 521.0156], [281.4509, 521.0156], [239.2634, 762.3281], [320.0223, 717.2344]]
	pose_pivot=[exit_pivot,freewoman_pivot, soccer_pivot]


	#정답 포즈 tan값
	tan_pivot=[]
	
	#player1, player2 tan값
	tan_data1=[]
	tan_data2=[]

	for i in range (0, len(pose_pivot[0])-1):
		print(self.key)
		tan_pivot.append(cal_tan(pose_pivot[self.key-1][i], pose_pivot[self.key-1][i+1]))
		tan_data1.append(cal_tan(pose_data1[i], pose_data1[i+1]))
		tan_data2.append(cal_tan(pose_data2[i], pose_data2[i+1]))


	#오차율 계산
	error1=abs(cal_error(tan_pivot, tan_data1, len(tan_pivot)))
	error2=abs(cal_error(tan_pivot, tan_data2, len(tan_pivot)))


	print('오차율: ',error1, error2)

	tan_pivot.clear()
	tan_data1.clear()
	tan_data2.clear()

	return error1, error2, flag


class poseQuiz(QWidget):
	start = 0
	
	def __init__(self):
		super().__init__()
		self.initUI()
		self.setFocusPolicy(Qt.StrongFocus)
		self.posetimer = QTimer(self)
		self.posetimer.setInterval(1000)
		self.posetimer.timeout.connect(self.timeout)
        
		self.buttontimer = QTimer(self)
		self.buttontimer.setInterval(100)
		self.buttontimer.timeout.connect(self.buttonClicked)
		self.buttontimer.start(0)

	def initUI(self):
		#포즈 퀴즈 UI
		self.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.504608, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(171, 225, 255, 255));")
		# 이미지 오브젝트 받아옴 (딕셔너리 형태)
		self.key = 0
		print("#########################")
        
		obj = QPixmap('/home/pi/Desktop/kt팀프로젝트/img/pose_main')
		obj = obj.scaledToHeight(800)
		self.img_label = QLabel()
		self.img_label.setPixmap(obj)
		self.img_label.setStyleSheet("background-color : transparent")
		self.img_label.setFixedHeight(850)
		self.img_label.setAlignment(Qt.AlignCenter)

		self.lcd = QLCDNumber()
		self.lcd.setDigitCount(2)
		self.lcd.setFixedWidth(200)
		self.lcd.setFixedHeight(100)
		self.lcd.setStyleSheet("""QLCDNumber {background-color: red;}""")

		self.timer = QTimer(self)
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.timeout)
		#self.count=2

		# UI layout
		self.vbox = QVBoxLayout()

		self.hbox = QHBoxLayout()

		self.title = QLabel('title')
		self.title.setFont(QFont('Arial', 50))
		self.title.setStyleSheet("background-color: rgba(0,0,0,0);")
		self.title.setAlignment(Qt.AlignHCenter)
		self.title.setVisible(False)

		self.desc = QLabel('description')
		self.desc.setFont(QFont('Arial', 30))
		self.desc.setStyleSheet("background-color: rgba(0,0,0,0);")
		self.desc.setAlignment(Qt.AlignHCenter)
		self.desc.setVisible(False)
		self.desc.setGeometry(1500,1100,400,200)

		self.vbox.setContentsMargins(0, 0, 0, 0)
		self.vbox.addWidget(self.title)
		self.vbox.addWidget(self.img_label)
		self.vbox.addWidget(self.desc)

		self.hbox.addLayout(self.vbox)
		self.setLayout(self.hbox)

		self.setWindowTitle('posing')

		self.showMaximized()

	#입력 event 처리
	def buttonClicked(self):
		global regame
		#입력 상황
		if self.start == 0:
			
			recog = kws.btn_test('기가지니')
			
			if recog == 200:
				

				self.count = 5
				self.title.setVisible(False)
				txt= subjects[self.key]
				self.key += 1
				self.img_label.setText(txt)
				self.img_label.setFont(QFont('Arial', 75))

				self.desc.setVisible(True)
				self.desc.setText('포즈를 취해주세요!')
				self.hbox.addWidget(self.lcd, 5, Qt.AlignTop)


				self.timer.start()
				self.repaint()
				if self.key >= 3:
					self.start = 1

		elif self.start == 1:
			recog = kws.btn_test('기가지니')
			if recog == 200:
				regame = 1
				app.quit()

	def keyPressEvent(self, e):
		global regame		
		if e.key() == Qt.Key_Space:
			regame = 1				
			self.close()
			app.quit()

	#카운트 종료 뒤 실행 되는 함수
	def timeout(self):
		self.count-=1
		self.lcd.display(self.count)
		if self.count== -1:
			self.timer.stop()
			self.lcd.display(0)
			
			while True:
				takePicture()
				result=analyzePose(self)
				
				if result[2]==0:
					sound.correctSound()
					break
			
			#정답 사진 공개 부분		
			self.desc.setVisible(False)
			self.title.setVisible(True)
			self.title.setText('정답공개')
			self.title.setAlignment(Qt.AlignCenter)
			answer_img=subjects_image[self.key-1]
			obj = QPixmap(answer_img)
			
			obj = obj.scaledToHeight(950)
			obj = obj.scaledToWidth(600)
			
			self.img_label.setPixmap(obj)
			self.repaint()
			
			time.sleep(2)
			
			#촬영 사진 공개 부분
			obj = QPixmap('photo.jpg')
			obj = obj.scaledToHeight(950)
			obj = obj.scaledToWidth(600)
			self.img_label.setPixmap(obj)
			self.title.setAlignment(Qt.AlignCenter)
			self.title.setText('촬영사진')
			
			self.desc.setVisible(True)
			
			if result[0]>result[1]: #player2가 이긴 경우
				self.desc.setText('player1 : 승   player2 : 패')
			else:
				self.desc.setText('player1 : 패   player2 : 승')
			
			#오차율 출력 => 오차율이 작은 경우 : 승/ 오차율이 큰 경우 : 패
			#self.desc.setText('오차율 : '+str(result[0])) #player1 오차율
			#self.desc.setText('오차율 : '+str(result[1])) #player2 오차율


#과일퀴즈 ui
form_class3 = uic.loadUiType("fruitmain.ui")[0]
form_class4 = uic.loadUiType("miss.ui")[0]

class fruitQuiz(QMainWindow, form_class3):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setFocusPolicy(Qt.StrongFocus)
		self.ftimer = QtCore.QTimer(self)
		self.ftimer.setInterval(100)
		self.ftimer.timeout.connect(self.buttonPressEvent)
		self.ftimer.start(0)

		
	def buttonPressEvent(self):
		global regame
		#입력 상황
		recog = kws.btn_test()
		if recog == 200:
			regame = 1
			app.quit()
			self.ftimer.stop()

	def keyPressEvent(self, e):
		#입력 상황
		if e.key() == Qt.Key_A:
			fwidget.setCurrentIndex(fwidget.currentIndex()+1)
			fwidget.setStyleSheet(
                "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.990244 rgba(132, 255, 200, 255));")
			print(fwidget.currentIndex())
			print("fruit")


class fruitQuiz2(QMainWindow, form_class4):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.ftimer2 = QtCore.QTimer(self)
		self.ftimer2.setInterval(100)
		self.ftimer2.timeout.connect(self.buttonPressEvent)
		self.ftimer2.start(0)

	def keyPressEvent(self, e):
		#입력 상황
		if e.key() == Qt.Key_A:
			fwidget.setCurrentIndex(fwidget.currentIndex()==0)
			print(fwidget.currentIndex())
			#self.ftimer2.stop()
			
	def buttonPressEvent(self):
		global regame
		
		recog = kws.btn_test()
		if recog == 200:
			regame = 1
			app.quit()
			self.ftimer2.stop()

class fruitQuiz3(QWidget):

	def __init__(self):
		super().__init__()
		self.label = QLabel(self)
		self.label.setStyleSheet("background-color : transparent")
		self.img_name = QLabel(self)
		self.img_name.setStyleSheet("background-color : transparent")
		self.questionNum = 10  # 출제 문제 갯수
		self.randList = self.random_List(self.questionNum, len(ansDict))
		self.ans = ansDict[0]
		self.ftimer3 = QtCore.QTimer(self)
		self.ftimer3.setInterval(100)
		self.ftimer3.timeout.connect(self.buttonPressEvent)
		self.ftimer3.start(0)
	
	def buttonPressEvent(self):
		global regame
		
		recog = kws.btn_test()
		if recog == 200:
			regame = 1
			app.quit()
			self.ftimer3.stop()

	def keyPressEvent(self, e):
		#입력 상황
		if e.key() == Qt.Key_A:
			#widget.setCurrentIndex(widget.currentIndex()==0)
			self.label.setVisible(False)
			self.quiz()
		
		if e.key() == Qt.Key_Space:
			self.quizStart(self.ans)
			self.label.setVisible(True)


	## 문제 출제 (1번 게임 코드 활용)
	def random_List(self, imageNum, maxImageNum):
		result = []

		for v in range(maxImageNum):
			result.append(v)
			random.shuffle(result)

		return result[0:imageNum]

	def makeQuiz(self):
		answerIndex = self.randList[-1]

		self.ans = ansDict[answerIndex]

		if not self.ans == 0:
			## 출력 부분 추가 (출력문 or UI) - 현경
			self.img_name.setText(str(self.ans) + ' 를 들고오세요.')
			self.img_name.setGeometry(150, 200, 1000, 300)
			self.img_name.setFont(QFont("210 오복상회 R", 70))  # 폰트,크기 조절
			self.img_name.setStyleSheet("Color : brown; background-color : transparent;")
			self.img_name.setAlignment(Qt.AlignCenter)

		else:
			return 1

	def quizStart(self, ans):
		while(True):
			time.sleep(3)
			#카메라 오픈
			command = "raspistill -t 1 -o test.jpg"  

			subprocess.call(command, shell = True)
			prediction = self.pred('test.jpg')  # 모델에 추론 이미지 인풋 -> 예측률 출력
			print(prediction)
			
			for i in range(len(ansDict) - 1):
				if prediction[0][i] >= 0.6:
					if ansDict[i] == ans:
						sound.correctSound()
						obj = QPixmap('test.jpg')
			
						obj = obj.scaledToHeight(950)
						obj = obj.scaledToWidth(600)
		
						self.label.setPixmap(obj)
						self.img_name.setGeometry(90, 500, 1000, 300)
						self.img_name.setText(ans + " 맞았습니다!")
						return
					else:
						sound.wrongSound()
						self.img_name.setGeometry(90, 500, 1000, 300)
						self.img_name.setText(ansDict[i] + " 틀렸습니다!")
						return
						

    ## 티처블 머신 학습된 모델 코드
	def pred(self, inference_data_path):  # .jpg 타입
		# Create the array of the right shape to feed into the keras model
		# The 'length' or number of images you can put into the array is
		# determined by the first position in the shape tuple, in this case 1.
		data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

		# Replace this with the path to your image
		image = Image.open(inference_data_path)

		# resize the image to a 224x224 with the same strategy as in TM2:
		# resizing the image to be at least 224x224 and then cropping from the center
		size = (224, 224)
		image = ImageOps.fit(image, size, Image.ANTIALIAS)

		# turn the image into a numpy array
		image_array = np.asarray(image)

		# display the resized image
		# image.show()

		# Normalize the image
		normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

		# Load the image into the array
		data[0] = normalized_image_array

        # run the inference
		prediction = model.predict(data)
        # print(prediction) ## 출력 결과 (각 Class별 확률값)pre

        ###prediction = [0, 0, 0.7, 0.3, 0]
        ###print(ans[0])

		return prediction

	def quiz(self):
		count = self.questionNum

		while count > 0:
			self.randList = self.random_List(self.questionNum, len(ansDict))

			self.makeQuiz()  ## makeQuiz() -> 내 quizStart() 작동 -> 그 안에서 정답판별 및 처리하는 구조,,

			count -= 1

if __name__ == '__main__':
	while regame == 1:
		regame = 0
		finish = 0
		app = QApplication(sys.argv)
		# 화면 전환용 Widget 설정
		widget = QtWidgets.QStackedWidget()
		fwidget = QtWidgets.QStackedWidget()
				
		# 레이아웃 인스턴스 생성
		Window =  gameStart()
		Window1 = Intro()
		Window2 = UIApp()
		Window3 = End()
		#Window4 = poseQuiz()
		
		
		# Widget 추가

		widget.addWidget(Window)
		widget.addWidget(Window1)
		widget.addWidget(Window2)
		widget.addWidget(Window3)

		print(widget)
		# 프로그램 화면을 보여주는 코드
		widget.showMaximized()
		print(widget.currentIndex())

		app.exec_()
		print("******************")
		del app
		del widget
		del Window
		del Window1
		del Window2
		del Window3
