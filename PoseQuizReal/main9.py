import sys
#import faulthandler; 
#faulthandler.enable()
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt,QPoint,QRectF
from PyQt5.QtCore import pyqtSignal, QObject

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QProcess, QRunnable, QThreadPool, QTimer, QTime

import time
import random
import ex1_kwstest2 as kws
import ex2_getVoice2Text2 as tts
import MicrophoneStream as MS
import urllib.request
import os
import sound
from PIL import Image
import requests
import subprocess

from io import StringIO

form_class0 = uic.loadUiType("gamemenu.ui")[0]
form_class1 = uic.loadUiType("intro.ui")[0]
form_class2 = uic.loadUiType("miss.ui")[0]


timerTimeSizeDefault = 10	#문제당 시간 
questionNum = 5	#출제 문제 갯수
global timerExitFlag

countTrue = 0
countFalse = 0
regame = 1
finish = 0

imageList=[]
randList=[]
answerList=[]

subjects = ["비상구", "자유의여신상", "축구선수"]
subjects_image=["/home/pi/Desktop/quiz2/img/answer_exit.jpg","/home/pi/Desktop/quiz2/img/answer_freewoman.jpg","/home/pi/Desktop/quiz2/img/answer_soccer.jpg"]

class gameStart(QMainWindow, form_class0):
	
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setFocusPolicy(Qt.StrongFocus)
		
	def keyPressEvent(self, e):
		if widget.currentIndex()==0:
			print("#########################")
			
			if e.key() == Qt.Key_A:
				widget.setCurrentIndex(widget.currentIndex()+1)
				print("#########################")		
				
			elif e.key() == Qt.Key_B:
				print("222222222222222222")
				self.www = poseQuiz()
				self.www.show()
				
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
				#print(imageList)

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
		#print(answerList)
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
		#quizImage.save(answer+"png")
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
			if self.count <= 0:
				quit()
			self.count -= 1
			
			recog = kws.btn_test('기가지니')		#버튼 입력
			if (recog == 200 and widget.currentIndex() == 3): #버튼입력 and "끝" 화면 상태 
				regame = 1
				self.timer4.stop()				
				self.close()
				app.quit()

		
		
class UIApp(QWidget):
	global questionNum, countTrue, countFalse, score, randList, answerList, person, imageList
	key = 0
	quizStart = 0	#퀴즈화면으
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
		'''★★★★★★★여기 추가 됐어요!!!!!!★★★★★★★★★★★'''
		#self.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")

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

		'''★★★★★★★여기 추가 됐어요!!!!!!★★★★★★★★★★★'''
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

		'''★★★★★★★여기 교체해주세요!!!!!!★★★★★★★★★★★'''
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
		#vbox.addWidget(self.img_name)

		self.setLayout(hbox)

		self.setWindowTitle('나영석PD')
		self.move(400,50)

		#self.show()
		self.showMaximized()

	#입력 event 처리
	def buttonClicked(self):
		global finish, regame, questionNum
		if self.stopbutton == 0 and widget.currentIndex()==2:
			
			recog = kws.btn_test('기가지니')		#버튼 입력
			
			if (recog == 200 and widget.currentIndex() == 2 and self.quizStart != 0): #버튼입력 and 2번째 UI and 퀴즈 준비화면 상태 
				self.stopbutton = 1
				#print(answerList) 
				#print(imageList)
				
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
	command = "raspistill -t 1 -o photo.jpg"   
	subprocess.call(command, shell = True)

#이미지 용량 축소
def resizeImg():
	file = 'photo.jpg'
	img = Image.open(file)
	img = img.resize((540, 780), Image.ANTIALIAS)
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

def cal_error(pivot, data, leng):
	err = 0
	for i in range (0,leng):
		err += pivot[i] - data[i]
	return err / leng

#포즈 분석 수행
def analyzePose(self):
	resizeImg() #용량 축소한 이미지 입력
	APP_KEY = 'cc945fdb4b2b7b18448576eeaaedca61'
	IMAGE_URL ='photo.jpg'
	IMAGE_FILE_PATH = 'photo.jpg'
	session = requests.Session()
	session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

	# URL로 이미지 입력시
	response = session.post('https://cv-api.kakaobrain.com/pose', data={'image_url': IMAGE_URL})
	#print(response.status_code, response.json())

	#이미지 파일 불러오기
	with open(IMAGE_FILE_PATH, 'rb') as f:
		response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', f)])
		print('응답코드',response.status_code, response.json())
		
		flag=0
		if len(response.json())==0 or len(response.json())==1:
			print('다시 촬영하겠습니')
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
		self.posetimer = QTimer(self)
		self.posetimer.setInterval(1000)
		self.posetimer.timeout.connect(self.timeout)
        
		self.buttontimer = QTimer(self)
		self.buttontimer.setInterval(100)
		self.buttontimer.timeout.connect(self.buttonClicked)
		self.buttontimer.start(0)

	def initUI(self):
		self.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.504608, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(171, 225, 255, 255));")
		# 이미지 오브젝트 받아옴 (딕셔너리 형태)
		self.key = 0
        
        
		obj = QPixmap('/home/pi/Desktop/quiz2/img/pose_main')
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
		self.title.setFont(QFont('Arial', 70))
		self.title.setStyleSheet("background-color: rgba(0,0,0,0);")
		self.title.setAlignment(Qt.AlignHCenter)
		self.title.setVisible(False)

		self.desc = QLabel('description')
		self.desc.setFont(QFont('Arial', 30))
		self.desc.setStyleSheet("background-color: rgba(0,0,0,0);")
		self.desc.setAlignment(Qt.AlignHCenter)
		self.desc.setVisible(False)

		self.vbox.setContentsMargins(0, 0, 0, 0)
		self.vbox.addWidget(self.title)
		self.vbox.addWidget(self.img_label)
		self.vbox.addWidget(self.desc)

		self.hbox.addLayout(self.vbox)
		self.setLayout(self.hbox)

		self.setWindowTitle('posing')
		#self.move(400, 50)

		self.showMaximized()

	#입력 event 처리
	def buttonClicked(self):
		global regame
		#입력 상황
		if self.start == 0:			
			recog = kws.btn_test('기가지니')			
			if recog == 200:				
				if self.key >= len(subjects):
					self.close()
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

		elif self.start == 1:
			recog = kws.btn_test('기가지니')
			if recog == 200:
				regame = 1
				app.quit()

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
					break
					
			self.desc.setVisible(False)
			self.title.setVisible(True)
			self.title.setText('정답공개')
			self.title.setAlignment(Qt.AlignCenter)
			answer_img=subjects_image[self.key-1]
			obj = QPixmap(answer_img)
			
			obj = obj.scaledToHeight(1500)
			obj = obj.scaledToWidth(1500)
			
			self.img_label.setPixmap(obj)
			self.repaint()
			
			time.sleep(2)
			obj = QPixmap('photo.jpg')
			self.img_label.setPixmap(obj)
			self.title.setText('촬영사진')
			
			self.desc.setVisible(True)
			
			if result[0]>result[1]: #player2가 이긴 경우
				self.desc.setText('player1 : 패   player2 : 승')
			else:
				self.desc.setText('player1 : 승   player2 : 패')
			
			#오차율 출력 => 오차율이 작은 경우 : 승/ 오차율이 큰 경우 : 패
			#self.desc.setText('오차율 : '+str(result[0])) #player1 오차율
			#self.desc.setText('오차율 : '+str(result[1])) #player2 오차율
	

if __name__ == '__main__':
	while regame == 1:
		regame = 0
		finish = 0
		app = QApplication(sys.argv)
		# 화면 전환용 Widget 설정
		widget = QtWidgets.QStackedWidget()
				
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
		#widget.addWidget(Window4)
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
