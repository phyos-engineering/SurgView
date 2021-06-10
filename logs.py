# !/usr/bin/env python
# title           :logs.py
# description     :Enter Description Here
# author          :Juan Maldonado
# date            :6/10/2021
# version         :0.0
# usage           :SEE README.md
# python_version  :3.7.10
# conda_version   :4.9.2
# ========================================================================================================
import datetime
import cv2 as cv
import os


class SessionLogger:
    def __init__(self):
        self.root_path = "logs/"
        self.curr_datetime = datetime.datetime.now()
        self.log_path = self.root_path + self.curr_datetime.strftime("%d_%m_%Y_%H_%M_%S")
        os.mkdir(self.log_path)

    def record_picture(self, image):
        curr_time = datetime.datetime.now()
        cv.imwrite(self.log_path + "/" + str(curr_time.strftime("%H_%M_%S")) + ".png", image)
