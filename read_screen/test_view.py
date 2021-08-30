"""
Unit tests for the mapping class
"""

from read_screen import view
import unittest
import cv2 as cv
import glob
import sys
from read_screen.extract import *
from read_screen.clean import *

#TODO:
# add tests for text extraction, ocr.space matching, map interface, etc.
# there is an issue with CircleCI, since it creates a docker container which might have a different directory so the
# tests that pass here using relative filepaths don't pass on CircleCI

class TestView(unittest.TestCase):
    pass

    # def test_clean_image(self):
    #     assert (True)
    #     img = clean_image(
    #     '../interface_assets/steris/home_page_templates/volume_up.jpg',
    #     # r'/Users/DanielFu/Desktop/All/PhyOS/SurgView/interface_assets/steris/home_page_templates/volume_up.jpg',
    #     show_results=True)
    #     show_result("Cleaned Image",img,is_enabled=True)
    #
    #
    # def test_pytesseract_extract_text(self):
    #     reader = view.UIReader()
    #     image_list = []
    #     extracted_text_list = []
    #     for filename in glob.glob('../interface_assets/steris/home_page_templates/*.jpg'):
    #         im = cv.imread(filename)
    #         image_list.append(im)
    #         # print(filename)
    #         # print(im)
    #         extracted_text = extract_text(im,"bottom_buttons_template",ocr = "pytesseract")
    #         extracted_text_list.append(extracted_text)
    #         # print(extracted_text)
    #     print(extracted_text_list)
    #     sys.stdout = extracted_text_list


