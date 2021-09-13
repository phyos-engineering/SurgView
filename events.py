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
# from speech import SpeechEngine
from view import UIReader
from controller import SerialController
from playsound import playsound
import azure_speech
import utils
import json
import platform
import multiprocessing
import requests
import json
import time
import logging
import datetime
from scribe import (
    LuisResponse,
    SessionLog,
    MappedWorkflow,
    MappedInterface,
    EnhancedJSONEncoder,
)


def get_time() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


class EventHandler:
    def __init__(self):
        """
        Constructor. Initializes SpeechEngine, UIReader and SerialController
        Classes
        """
        self.speech_engine = azure_speech.SpeechEngine()
        self.interface_reader = UIReader()
        self.serial_controller = SerialController()
        self.intent_accuracy_threshold = 0.50  # TO DO: I'm not completely
        # confident with this value
        self.intent_state = None  # TO DO: Think of a better name?
        self.source = []  # TO DO:  Think of a better name?
        self.destinations = []
        self.workflow = []

        # OS System Info
        self.system_name = platform.system()
        self.system_release = platform.release()
        self.system_version = platform.version()

        # Hardware Info
        self.device_serial_number = utils.get_serial_number()
        self.board_model = utils.get_board_model()
        self.processor_name = platform.processor()
        self.processor_cores = multiprocessing.cpu_count()
        self.device_memory = "4GB"

        # Software Info
        self.python_version = platform.python_version()
        self.python_compiler = platform.python_compiler()
        self.python_impl = platform.python_implementation()
        self.application_version = "0.01"

        self.session_log = SessionLog(get_time())

        self.num_interface_mappings = 0
        self.num_mapped_workflows = 0
        self.num_luis_requests = 0

        # Device Status
        self.is_online = True
        self.interface_reader.query_frame()
        self.interface_reader.map_interface()

        # Log First Scan
        self.session_log.mapped_interfaces.append(
            MappedInterface(
                self.num_interface_mappings + 1,
                get_time(),
                self.interface_reader.gui_map.get_map(),
            )
        )
        self.num_interface_mappings += 1

        # print(self.register_device())
        # self.register_device()
        # self.check_if_registered()

    def listen(self):
        """
        Listen for activation word and prompt user with sound to give voice
        command.
        """
        keep_listening = True
        while keep_listening:
            print("Listening for Activation Word...")
            if self.speech_engine.recognize_keyword():
                # playsound("prompt.mp3")
                response = self.speech_engine.recognize_intent()
                json_payload = json.loads(response)
                print(json_payload)
                self.process_intent(json_payload)
                self.session_log.luis_ai_responses.append(
                    LuisResponse(self.num_luis_requests + 1, get_time(), json_payload)
                )
                self.num_luis_requests += 1

    def check_if_registered(self):
        url = "http://192.168.0.152:8000/api/device/check"
        payload = {"serialNumber": self.device_serial_number}
        result = requests.get(url, params=payload)
        if result.text == "false":
            self.register_device()

    def register_device(self):
        url = "http://192.168.0.152:8000/api/device"
        headers = {"Content-Type": "application/json", "Accept": "json"}
        obj = {
            "serialNumber": self.device_serial_number,
            "boardModel": self.board_model,
            "processorName": self.processor_name,
            "processorCores": self.processor_cores,
            "deviceMemory": self.device_memory,
            "systemName": self.system_name,
            "systemRelease": self.system_release,
            "systemVersion": self.system_version,
            "pythonVersion": self.python_version,
            "pythonCompiler": self.python_compiler,
            "pythonImplementation": self.python_impl,
            "applicationVersion": self.application_version,
            "online": self.is_online,
        }
        result = requests.post(url, data=json.dumps(obj), headers=headers)
        logging.debug(result.headers)

    def process_intent(self, luis_ai_response: json):
        """
        Process intent returned by LUIS.ai after voice command was given at
        prompt.
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
        self.interface_reader.query_frame()
        self.interface_reader.map_interface()

        # Log Mapping
        self.session_log.mapped_interfaces.append(
            MappedInterface(
                self.num_interface_mappings + 1,
                get_time(),
                self.interface_reader.gui_map.get_map(),
            )
        )
        self.num_interface_mappings += 1

    def check_diff(self):
        self.interface_reader.check_diff()

    def build_workflow(self):
        """
        Combine identified sources and destination
        """
        source_labels = []
        destination_labels = []
        label_worfklow = []
        for items in self.source:
            source_labels.append(items[0])

        for items in self.destinations:
            destination_labels.append(items[0])

        label_worfklow += source_labels + destination_labels

        self.session_log.mapped_workflows.append(
            MappedWorkflow(
                self.num_mapped_workflows + 1,
                self.num_luis_requests,
                self.num_interface_mappings,
                get_time(),
                label_worfklow,
            )
        )
        self.num_mapped_workflows += 1

        self.workflow += self.source + self.destinations

    def source_to_destination(self):
        """
        Process workflow for SourceToDestination Intent
        """
        entities = self.intent_state["entities"]

        # self.add_dummy_values()  # Testing

        # First check for existence of a source and destination
        for entity in entities:
            if entity["type"] == "source":
                to_int_label = utils.transform_to_int(entity["entity"])
                source_label = utils.clean_string(to_int_label)

                button = self.interface_reader.gui_map.locate_label(source_label)

                if button is not None:
                    self.source.append(button)

            if entity["type"] == "destination":
                to_int_label = utils.transform_to_int(entity["entity"])
                destination_label = utils.clean_string(to_int_label)

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

    def update_status(self):
        url = "http://192.168.0.152:8000/api/device/update"
        headers = {"Content-Type": "application/json", "Accept": "json"}
        online_status = None
        if self.is_online:
            online_status = False
        else:
            online_status = True

        obj = {"serialNumber": self.device_serial_number, "online": online_status}
        result = requests.patch(url, data=json.dumps(obj), headers=headers)
        logging.debug(result.headers)

    def shutdown(self):
        print("Shutting Down...")
        json_log = json.dumps(self.session_log, cls=EnhancedJSONEncoder, indent=4)
        with open(
            self.interface_reader.session_logger.log_path + "/session.json", "w"
        ) as outfile:
            outfile.write(json_log)

        print(json_log)
        # self.update_status()
        exit(0)

    def match_case(self, intent: str):
        """
        Switch statement in Python via dictionaries
        :param intent: LUIS.ai intent
        :return: method that should be executed by process_intent()
        """
        switch = {
            "MapInterface": self.map_interface,
            "SourceToDestination": self.source_to_destination,
            "SelectButton": self.select_button,
            "Shutdown": self.shutdown,
            "CheckDifference": self.check_diff,
        }

        command_function = switch.get(intent, lambda: self.default_response)
        return command_function

    def execute_workflow(self, flag: int):
        self.build_workflow()
        if flag == 0:
            for i in self.workflow:
                # print("Moving Mouse: {} {}".format(i[1]["x"], i[1]["y"]))
                self.serial_controller.move_mouse(i[1]["x"], i[1]["y"])
            # Clean Workflow
            self.workflow.clear()
            self.source.clear()
            self.destinations.clear()
        if flag == 1:
            self.serial_controller.type_with_keyboard("Hello World!")
            # Clean Workflow
