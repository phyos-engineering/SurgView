# !/usr/bin/env python
# title           :events.py
# description     :Enter Description Here
# author          :Juan Maldonado
# date            :5/10/2021
# version         :0.0
# usage           :SEE README.md
# python_version  :3.7.10
# conda_version   :4.9.2
# ====================================================================================================================
from speech import SpeechEngine
from view import UIReader
from controller import SerialController
from playsound import playsound
import json


class EventHandler:
	def __init__(self):
		"""
		Constructor. Initializes SpeechEngine, UIReader and SerialController Classes
		"""
		self.speech_engine = SpeechEngine()
		self.interface_reader = UIReader()
		# self.serial_controller = SerialController()
		self.intent_accuracy_threshold = 0.50

	def listen(self):
		"""
		Listen for activation word and prompt user with sound to give voice command.
		"""
		keep_listening = True
		while keep_listening:
			if self.speech_engine.detect_activation_word():
				playsound("prompt.mp3")
				self.process_intent(self.speech_engine.recognize_intent())

	def process_intent(self, intent_result: json):
		intent_score = intent_result["topScoringIntent"]["score"]
		if intent_score >= self.intent_accuracy_threshold:
			intent = intent_result["topScoringIntent"]["intent"]

			if intent == "ScanInterface":
				self.interface_reader.capture_feed()
				self.interface_reader.map_interface()

		return

	def execute_workflow(self, flag: int):
		if flag == 0:
			self.serial_controller.move_mouse()
		if flag == 1:
			self.serial_controller.type_with_keyboard()
