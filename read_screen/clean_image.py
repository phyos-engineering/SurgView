# title           :clean_image.py
# description     :Image cleaning functions
# author          :Dan Fu
# date            :08/18/2021
# version         :0.0
# usage           :SEE README.md
# python_version  :3.7.10
# conda_version   :4.10.3
# ========================================================================================================

from . import view
import cv2 as cv
import os

'''
clean_image.py
Takes an image or filepath as input and returns a cleaned version of whichever input it's given
Contains:
    clean_image() which parses image or filepath 
    image_cleaner() which converts to greyscale and applies a threshold to the image
'''

def clean_image(image_or_filepath, show_results:bool = False):

    if isinstance(image_or_filepath, str):
        # Open a file as an image
        filepath = image_or_filepath
        image = cv.imread(filepath)

        # Clean the image
        image_gray_threshold = image_cleaner(image, show_results)

        # Save the cleaned image in the same directory with the same filename
        directory = os.path.split(filepath)[0]
        filename = os.path.split(filepath)[1]
        os.chdir(directory) # change to the same directory as the filepath
        cv.imwrite(filename,image_gray_threshold)

    else:
        image = image_or_filepath
        image_gray_threshold = image_cleaner(image, show_results)
        return image_gray_threshold

def image_cleaner(image, show_results):

    # Read Image
    reader = view.UIReader()
    reader.show_result("Target image", image, show_results)

    # Covert to Grayscale
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    reader.show_result("Target Image In Grayscale", image_gray, show_results)

    # Apply Threshold
    ret, image_gray_threshold = cv.threshold(image_gray, 127, 255, 0)
    reader.show_result("Grayscale image with a threshold applied", image_gray_threshold,
                     show_results)

    return image_gray_threshold