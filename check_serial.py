import time
import serial
from controller import SerialController

ser = SerialController()
ser.move_mouse(1, 1)
