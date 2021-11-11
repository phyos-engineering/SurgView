# !/usr/bin/env python
# title           :controller.py
# description     :Class in charge of establishing communication between Arduino Leonardo and Pi4.
# author          :Sebastian Maldonado
# date            :5/13/21
# version         :0.0
# usage           :SEE README.md
# notes           :Enter Notes Here
# python_version  :3.6.8
# conda_version   :4.8.3
# =================================================================================================================
from serial import Serial
"""
The SerialController class allows us to interface with the Arduino Leonardo board via serial communication.
"""
import time
import asyncio


class SerialController:
    def __init__(self):
        """
		Constructor. Assigns serial port USB0 as communication medium between Arduino Leonardo and Pi4.
		"""
        self.serial_controller = Serial(port='/dev/ttyUSB0',
                                        baudrate=9600,
                                        timeout=None)
        self.serial_controller.flush()

    async def read_arduino_buffer(self):
        response = self.serial_controller.readline().decode('utf-8').rstrip()
        return response

    async def send_payload_to_board(self, x_coordinate: int,
                                    y_coordinate: int):
        """
		Sends command, in byte format, to Arduino Leonardo to move mouse.
		:param x_coordinate: X screen coordinate of target widget.
		:param y_coordinate: Y screen coordinate of target widget.
		"""
        mouse_command = "{} {} {} {}\n".format("mouse", x_coordinate,
                                               y_coordinate, 0)
        bytes_written = self.serial_controller.write(
            bytes(mouse_command, 'utf-8'))
        board_response = self.read_arduino_buffer()

        arduino_response = await board_response
        print(arduino_response)
        self.serial_controller.reset_input_buffer()
        self.serial_controller.reset_output_buffer()

    def move_mouse(self, x_coordinate: int, y_coordinate: int):
        asyncio.run(self.send_payload_to_board(x_coordinate, y_coordinate))

    def type_with_keyboard(
            self, text_content: str):  # TO DO: Fix how Arduino parses string.
        """
		Sends command, in byte format, to Arduino Leonardo to type text.
		:param text_content: Text intended to fill a text field.
		"""
        keyboard_command = "{} {}\n".format("keyboard", text_content)
        self.serial_controller.write(bytes(keyboard_command, 'utf-8'))

        arduino_response = self.serial_controller.readline().decode(
            'utf-8').rstrip()
        print(arduino_response)
