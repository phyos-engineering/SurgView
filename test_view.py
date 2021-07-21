"""
Unit tests for the mapping class
"""

import view
import unittest
import cv2 as cv
import glob
import pytesseract

class TestView(unittest.TestCase):

    def test_OCR_accuracy(self):
        reader = view.UIReader()
        image_list = []
        extracted_text_list = []
        for filename in glob.glob('/Users/DanielFu/Desktop/All/PhyOS/SurgView/interface_assets/steris/home_page_templates/*.jpg'):
            im = cv.imread(filename)
            image_list.append(im)
            # print(filename)
            # print(im)
            extracted_text = reader.extract_text(im,"bottom_buttons_template")
            extracted_text_list.append(extracted_text)
            # print(extracted_text)
        print(extracted_text_list)
        # sys.stdout = extracted_text_list


