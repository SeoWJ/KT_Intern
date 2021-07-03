import time
import random
import ex1_kwstest2 as kws
import ex2_getVoice2Text2 as tts
import ex6_queryVoice as dss
import MicrophoneStream as MS
import threading
import csv
import os
import cv2
import sound
from PIL import Image



timerTimeSizeDefault = 10	#문제당 시간 
questionNum = 10	#출제 문제 갯수
global answerList
global timerExitFlag
countTrue = 0
countFalse = 0
semaphore = threading.Semaphore(1)

combo = 0
score = 0

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
	global answerList
	
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
				wrong_image = cv2.imread('audios/wrong_image.jpg')
				sound.wrongSound()
				countFalse += 1
				combo = 0
				cv2.imshow('Wrong', wrong_image)
				cv2.waitKey(1000)
				print("Wrong")
				cv2.destroyAllWindows()
				
			print("정답 갯수: " + str(countTrue))
			print("오답 갯수: " + str(countFalse))
			print("정답률: " + str(countTrue/questionNum*100) +  '%')
			print("점수:  " +str(score) + '점')
			
			semaphore.acquire()	
			timerExitFlag = 1
			semaphore.release()
			
	time.sleep(3)
		
	
	
#kws.test('기가지니')
while 1:			
	time.sleep(0.2)								#호출어(기가지니)로 프로그램 실행 
	if tts.getVoice2Text().find("기가지니")>=0:
		break
		

	
readData()
randList = random_List(questionNum, len(answerList))
	
#print(randList)

count = questionNum

while count > 0:
	
	makeQuiz()
	count-=1

print("정답 갯수: " + str(countTrue))
print("오답 갯수: " + str(countFalse))
print("정답률: " + str(countTrue/questionNum*100) +  '%')
print("점수:  " +str(score) + '점')
del answerList
