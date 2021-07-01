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
from datetime import datetime
import cv2 as cv
import os
import hashlib
import utils


class SessionLogger:
    def __init__(self):
        self.root_path = "logs/"
        self.now = datetime.now()
        self.session_id = utils.get_serial_number() + "_" + self.now.strftime(
            "%m-%d-%Y_%H:%M:%S")
        self.session_date = self.now.date().strftime("%m-%d-%Y")

        self.log_path = self.root_path + self.now.strftime(
            "%m_%d_%Y_%Hh_%Mm_%Ss")
        os.mkdir(self.log_path)

    def record_picture(self, image, image_title):
        now = datetime.now()
        cv.imwrite(self.log_path + "/" + image_title + ".png", image)
