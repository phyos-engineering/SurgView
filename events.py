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
import utils
import json


class EventHandler:
    def __init__(self):
        """
        Constructor. Initializes SpeechEngine, UIReader and SerialController Classes
        """
        self.speech_engine = SpeechEngine()
        self.interface_reader = UIReader()
        # self.serial_controller = SerialController()
        self.intent_accuracy_threshold = 0.50  # TO DO: I'm not completely confident with this value
        self.intent_state = None  # TO DO: Think of a better name?
        self.source = []  # TO DO:  Think of a better name?
        self.destinations = []
        self.workflow = []

    def listen(self):
        """
        Listen for activation word and prompt user with sound to give voice command.
        """
        keep_listening = True
        while keep_listening:
            if self.speech_engine.detect_activation_word():
                playsound("prompt.mp3")
                self.process_intent(self.speech_engine.recognize_intent())

    def process_intent(self, luis_ai_response: json):
        """
        Process intent returned by LUIS.ai after voice command was given at prompt.
        :param luis_ai_response: JSON file containing
        """

        # Update Intent State
        self.intent_state = luis_ai_response

        # Extract Intent Probability Score (Higher == Better)
        intent_score = self.intent_state["topScoringIntent"]["score"]

        # Ignore intent with low probability score
        if intent_score >= self.intent_accuracy_threshold:
            intent = self.intent_state["topScoringIntent"]["intent"]

            # S
            funct = self.match_case(intent)
            # Fire function
            funct()

    def add_dummy_values(self):
        self.interface_reader.gui_map.add_widget("4ksurgicaldisplay1", 1, 2)
        self.interface_reader.gui_map.add_widget("vitals", 3, 4)

    def map_interface(self):
        print("Mapping Interface...")
        self.interface_reader.capture_feed()
        self.interface_reader.map_interface()

    def build_workflow(self):
        """
        Combine identified sources and destination
        """
        self.workflow += self.source + self.destinations

    def source_to_destination(self):
        """
        Process workflow for SourceToDestination Intent
        """
        entities = self.intent_state["entities"]

        self.add_dummy_values()  # Testing

        # First check for existence of a source and destination
        for entity in entities:
            if entity['type'] == 'source':
                source_label = utils.clean_string(entity['entity'])
                button = self.interface_reader.gui_map.locate_label(source_label)

                if button is not None:
                    self.source.append(button)

            if entity['type'] == 'destination':
                destination_label = utils.clean_string(entity['entity'])
                button = self.interface_reader.gui_map.locate_label(destination_label)

                if button is not None:
                    self.destinations.append(button)

        # They both exist so lets run a workflow
        if self.source is not None and self.destinations is not None:
            self.execute_workflow(0)
        else:
            print("No workflow to process")

    def default_response(self):
        print("Intent Not Found")

    def select_button(self):
        print("Selecting Button...")

    def match_case(self, intent: str):
        """
        Switch statement in Python via dictionaries
        :param intent: LUIS.ai intent
        :return: method that should be executed by process_intent()
        """
        switch = {"MapInterface": self.map_interface,
                  "SourceToDestination": self.source_to_destination,
                  "SelectButton": self.select_button}

        command_function = switch.get(intent, lambda: self.default_response)
        return command_function

    def execute_workflow(self, flag: int):
        self.build_workflow()
        if flag == 0:
            for i in self.workflow:
                print("Moving Mouse: {} {}".format(i[1]["x"], i[1]["y"]))
                # self.serial_controller.move_mouse(i[1]["x"], i[1]["y"])
        if flag == 1:
            self.serial_controller.type_with_keyboard()
