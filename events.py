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


class EventHandler:
	def __init__(self):
		"""
		Constructor. Initializes SpeechEngine, UIReader and SerialController Classes
		"""
		self.speech_engine = SpeechEngine()
		self.interface_reader = UIReader()
		self.serial_controller = SerialController()

	def listen(self):
		return

	def process_intent(self):
		return

	def execute_workflow(self, flag: int):
		if flag == 0:
			self.serial_controller.move_mouse()
		if flag == 1:
			self.serial_controller.type_with_keyboard()
