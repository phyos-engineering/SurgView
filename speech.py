# !/usr/bin/env python
# title           :speech.py
# description     :Speech Engine Class
# author          :Juan Maldonado
# date            :5/10/2021
# version         :0.0
# usage           :python speech.py
# python_version  :3.7.10
# conda_version   :4.9.2
# ====================================================================================================================
from azure.cognitiveservices.speech import SpeechConfig
from azure.cognitiveservices.speech import KeywordRecognitionModel
from azure.cognitiveservices.speech import KeywordRecognizer
from azure.cognitiveservices.speech import ResultReason
from azure.cognitiveservices.speech.intent import IntentRecognizer
from azure.cognitiveservices.speech.intent import LanguageUnderstandingModel
from azure.cognitiveservices.speech.audio import AudioConfig
from azure.cognitiveservices.speech import PropertyId

import json
import unittest

# API KEYS (To Do: Load as config file at start)
SPEECH_KEY = "b6ad1d58ae084ca08e3f3d753ab18e0b"
SERVICE_REGION = "westus"
APP_ID = "9aa263e1-f530-47ec-ae77-7b9b694463bc"

"""
The Speech Engine class parses a surgeon's voice for voice commands or activation word using 
Microsoft LUIS.ai and Microsoft Cognitive Services.
"""


class SpeechEngine:
	def __init__(self):
		"""
		Constructor configures and initializes intent and keyword recognizers.
		"""
		# LUIS.ai Parser Configuration
		self.intent_config = SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)  # Configure Spec
		self.model = LanguageUnderstandingModel(app_id=APP_ID)  # Load LUIS.ai Model
		self.intent_recognizer = IntentRecognizer(speech_config=self.intent_config)
		self.intent_recognizer.add_all_intents(model=self.model)

		# Speech Studio Custom Keyword Configuration
		self.keyword_model = KeywordRecognitionModel("1bccce7e-f4de-475b-ba2f-9eb9abaa1e08.table")  # Load Keyword
		# Model
		self.keyword_audio_config = AudioConfig(use_default_microphone=True)  # Configure Audio Input
		self.keyword_recognizer = KeywordRecognizer(audio_config=self.keyword_audio_config)

	def recognize_intent(self):
		"""
		Sends voice command to LUIS.ai and returns response containing matched intent.
		"""
		response = self.intent_recognizer.recognize_once()
		if response.reason == ResultReason.RecognizedIntent:
			return json.loads(response.properties.get(PropertyId.LanguageUnderstandingServiceResponse_JsonResult))

	def detect_activation_word(self):
		"""
		Listens (but not records) for activation word (WAKE UP).
		:return: Boolean Value: True -> Keyword Recognized, False -> Keyword Not Recognized
		"""
		keyword_result = self.keyword_recognizer.recognize_once_async(self.keyword_model).get()
		return True if keyword_result.reason == ResultReason.RecognizedKeyword else False


def main():
	# ADD TESTS HERE (Dan)
	engine = SpeechEngine()
	print("Say something...")
	print(engine.detect_activation_word())
	print("Say something...")
	print(engine.recognize_intent())


if __name__ == "__main__":
	main()
