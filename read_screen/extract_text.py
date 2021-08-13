import time
import cv2 as cv
import utils
import logging
import pytesseract
import re

#TODO: implement ocr.space with filepath and image, also fix ocr param, ocr = "ocr.space",

def extract_text(image_or_filepath,
                 flag: str) -> str:  # TO DO: Pass filepath or mat?
    """
    Extract text from an image using Google Tesseract.
    :param extracted_image: button image returned by contour mapping
    :param flag:
    """
    start_time = time.time()
    # Enlarge image (helps with OCR accuracy)
    enlarged_image = cv.resize(src=extracted_image,
                               dsize=(0, 0),
                               fx=3,
                               fy=3)
    # We need the image in grayscale to apply thresholding

    # We can't extract a label from the main window
    if flag == "main_window_template":
        return "fullscreen"

    threshold = None

    # Apply different thresholding technique based on button's features
    if flag == "bottom_buttons_template":
        enlarged_image = cv.resize(src=extracted_image,
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
            image=extracted_image.copy(), config='--psm 6')
    if threshold is not None:
        extracted_text = pytesseract.image_to_string(
            image=threshold.copy(), config='--psm 3')

    # Remove punctuation and etc from string
    cleaned_text = utils.clean_string(extracted_text)
    cleaned_text = re.sub('sre.*', '', cleaned_text)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Extracting Text: {} - Elapsed Time: {}s".format(
        cleaned_text, round(elapsed_time, 2)))

    logging.debug("Extracting Text: {} - Elapsed Time: {}s".format(
        cleaned_text, round(elapsed_time, 2)))
    return cleaned_text