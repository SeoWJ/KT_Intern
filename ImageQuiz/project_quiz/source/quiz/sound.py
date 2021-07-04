#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 1: GiGA Genie Keyword Spotting"""

from __future__ import print_function
import time
import audioop
from ctypes import *
import RPi.GPIO as GPIO
import ktkws # KWS
import MicrophoneStream as MS

RATE = 16000
CHUNK = 512


	
def correctSound():

	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		#audio_generator = stream.generator()
		MS.play_file("audios/correct.wav") 

def wrongSound():

	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		#audio_generator = stream.generator()
		MS.play_file("audios/wrong.wav")

		
#while 1:
#	correctSound()
