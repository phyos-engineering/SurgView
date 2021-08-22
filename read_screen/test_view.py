"""
Unit tests for the mapping class
"""

from read_screen import view
import unittest
import cv2 as cv
import glob
from read_screen.extract import *
from read_screen.clean import *


class TestView(unittest.TestCase):

#TODO: Fix filepath to start with /

    def test_clean_image(self):
        img = clean_image(
        r'/Users/DanielFu/Desktop/All/PhyOS/SurgView/interface_assets/steris/home_page_templates/volume_up.jpg',
        show_results=True)
        # show_result("Cleaned Image",img,is_enabled=True)
        assert(True)

    def test_pytesseract_extract_text(self):
        reader = view.UIReader()
        image_list = []
        extracted_text_list = []
        for filename in glob.glob('/Users/DanielFu/Desktop/All/PhyOS/SurgView/interface_assets/steris/home_page_templates/*.jpg'):
            im = cv.imread(filename)
            image_list.append(im)
            # print(filename)
            # print(im)
            extracted_text = extract_text(im,"bottom_buttons_template",ocr = "pytesseract")
            extracted_text_list.append(extracted_text)
            # print(extracted_text)
        print(extracted_text_list)
        # sys.stdout = extracted_text_list



