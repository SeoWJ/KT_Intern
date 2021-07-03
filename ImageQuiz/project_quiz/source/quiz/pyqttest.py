import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QProcess

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

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MySignal(QObject):
	signal1 = pyqtSignal()
	signal2 = pyqtSignal(int, int)

	def run(self):
		
		self.signal1.emit()
		self.signal2.emit(1, 2) 



class MyWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		mysignal = MySignal()
		mysignal.signal1.connect(self.signal1_emitted)
		mysignal.signal2.connect(self.signal2_emitted)
		mysignal.run()

	@pyqtSlot()
	def signal1_emitted(self):
		
		print("button")
		print("signal1 emitted")
        

	@pyqtSlot(int, int)
	def signal2_emitted(self, arg1, arg2):
		print("signal2 emitted", arg1, arg2)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
