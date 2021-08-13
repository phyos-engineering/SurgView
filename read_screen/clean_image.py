from . import view
import cv2 as cv

def clean_image(image_or_filepath, show_results:bool = False):

    '''
    an image is not a string, correct?
    '''

    if isinstance(image_or_filepath, str):
        filepath = image_or_filepath
        # open a file as an image, image_cleaner(image), save the cleaned image to the same filepath
    else:
        image = image_or_filepath
        image_cleaner(image, show_results)

def image_cleaner(image, show_results):
    reader = view.UIReader()
    # Read Image
    reader.show_result("Target image", image, show_results)

    # Covert to Grayscale
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    reader.show_result("Target Image In Grayscale", image_gray, show_results)

    # Apply Threshold
    ret, image_gray_threshold = cv.threshold(image_gray, 127, 255, 0)
    reader.show_result("Grayscale image with a threshold applied", image_gray_threshold,
                     show_results)

    return image_gray_threshold