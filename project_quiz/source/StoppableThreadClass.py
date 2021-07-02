import ex1_kwstest as kws
import ex4_getText2VoiceStream as tts
import ex6_queryVoice as dss
import MicrophoneStream as MS
import time
import threading

class StoppableThreadClass(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.event = threading.Event() # <---- Added
		
	def run(self):
		while not self.event.is_set(): # <---- Added
			self.checkButton
			self.event.wait(self.checkButton) # <---- Added ( Time to repeat moved in here )
			
	def stop(self):       # <---- Added ( ease of use )
		self.event.set()  # <---- Added ( set to False and causes to stop )
		
	def checkButton(self):
		recog = kws.btn_test('기가지니')
		
		if recog == 200:
			print('KWS Dectected ...\n Start STT...')
			# 음성인식 파트. 현경씨 코드
			# 이후 음성인식 결과를 바탕으로 정답확인 파트. 소정씨 코드
		else:
			print('KWS Not Dectected ...')
			
	def get_status(self):
		return self.last_status
