import time
import cv2 as cv
import utils
import logging
import pytesseract
import re

#TODO: implement extract text using ocr.space with filepath and image

def extract_text(image_or_filepath,
                 flag: str,
                 ocr = "ocr.space") -> str:
    """
    Extract text from an image using Google Tesseract.
    :param extracted_image: button image returned by contour mapping
    :param flag:
    :param ocr: selects ocr.space or pytesseract
    """
    start_time = time.time()

    # We can't extract a label from the main window
    if flag == "main_window_template":
        return "fullscreen"

    # Check if we have an image or a filepath
    if isinstance(image_or_filepath, str):
        # Open a file as an image
        filepath = image_or_filepath
        image = cv.imread(filepath)

        # Extract the text from the image
        return text_extracter(image,ocr,flag,start_time)
        # Return extracted text

    else:
        image = image_or_filepath
        return text_extracter(image,ocr,flag,start_time)

def text_extracter(image,ocr,flag,start_time):
    if ocr.lower() == "ocr.space" or ocr.lower() == "ocr space" or ocr.lower() == "ocr_space":
        return ocr_space_text_extracter(image,start_time)
    if ocr.lower() == "pytesseract" or ocr.lower() == "tesseract":
        return py_text_extracter(image,flag,start_time)
    return ocr_space_text_extracter(image,start_time)

def ocr_space_text_extracter(image,start_time):

    #TODO: ocr_space_text_extracter

    cleaned_text = "TODO"
    print(f"Extracting Text: {cleaned_text} ocr.space Elapsed Time: {elapsed_time(start_time)}")
    logging.debug(f"Extracting Text: {cleaned_text} ocr.space Elapsed Time: {elapsed_time(start_time)}")

    return cleaned_text

def py_text_extracter(image,flag,start_time):
    # Enlarge image (helps with OCR accuracy)
    enlarged_image = cv.resize(src=image,
                               dsize=(0, 0),
                               fx=3,
                               fy=3)
    # We need the image in grayscale to apply thresholding
    threshold = None

    # Apply different thresholding technique based on button's features
    if flag == "bottom_buttons_template":
        enlarged_image = cv.resize(src=image,
                                   dsize=(0, 0),
                                   fx=9,
                                   fy=9)

        gray_image = cv.cvtColor(enlarged_image.copy(), cv.COLOR_BGR2GRAY)
        threshold = cv.threshold(src=gray_image,
                                 thresh=127,
                                 maxval=255,
                                 type=cv.THRESH_BINARY_INV)[1]
    # self.show_result("ButtonThreshold", threshold, 1)

    # final_image = cv.medianBlur(src=final_image, ksize=1)

    # Run OCR on image
    extracted_text = None
    if threshold is None:
        extracted_text = pytesseract.image_to_string(
            image=image.copy(), config='--psm 6')
    if threshold is not None:
        extracted_text = pytesseract.image_to_string(
            image=threshold.copy(), config='--psm 3')

    # Remove punctuation and etc from string
    cleaned_text = utils.clean_string(extracted_text)
    cleaned_text = re.sub('sre.*', '', cleaned_text)

    print(f"Extracting Text: {cleaned_text} Pytesseract Elapsed Time: {elapsed_time(start_time)}")
    logging.debug(f"Extracting Text: {cleaned_text} Pytesseract Elapsed Time: {elapsed_time(start_time)}")

    return cleaned_text

def elapsed_time(start_time):
    return round(time.time() - start_time,2)