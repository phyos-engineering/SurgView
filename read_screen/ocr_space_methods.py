# title           :ocr_space_methods.py
# description     :methods related to the ocr.space algorithm image parsing and extraction of words/locations
# author          :Dan Fu
# last modified   :08/29/2021
# version         :0.0
# usage           :see below
# python_version  :3.7.10
# conda_version   :4.9.2
# ========================================================================================================

import requests
import jsbeautifier
import json
import math

"""
Methods for ocr.space algorithm image parsing and extraction of words/locations, includes:
    1. parse_loc() parses the location of the center of the first word 
       in a line of text from the json file output generated from ocr.space
    2. make_beautified_json() makes a json, beautifies it, and then returns the name of that json
    3. ocr_space_text_map() extracts the words in each lines and their locations
    4. ocr_request_error() checks if there was an error in processing the image on ocr.space
       and prints an error message if there was
    5. ocr_space_file_request() OCR.space API request with local file
       This code was found on Github
       https://github.com/Zaargh/ocr.space_code_example/blob/master/ocrspace_example.py
"""

def parse_loc(loc_of_first_word_in_line):
    # parses the location of the center of the first word in a line of text from the json file output generated from ocr.space
    pixels_from_left_side_of_image = loc_of_first_word_in_line["Left"]
    pixels_from_top_side_of_image = loc_of_first_word_in_line["Top"]
    pixels_width_of_image = loc_of_first_word_in_line["Width"]
    pixels_height_of_image = loc_of_first_word_in_line["Height"]
    x_center_coord = pixels_from_left_side_of_image+ math.floor(pixels_width_of_image/2)
    y_center_coord = pixels_from_top_side_of_image + math.floor(pixels_height_of_image/2)
    return x_center_coord,y_center_coord

def make_beautified_json(parsed_result,target_image_filename):
    # makes a json, beautifies it, and then returns the name of that json
    fn = target_image_filename
    # creates a one-line json file with the parsed result
    jsonFile = open(fn + ".json", "w")
    jsonFile.write(parsed_result)
    jsonFile.close()
    # overwrites that same one-line json file with a human-readable result
    res = jsbeautifier.beautify_file(fn + ".json")
    jsonFile = open(fn + ".json", "w")
    jsonFile.write(res)
    jsonFile.close()
    # reads each json file and parses the center coordinates of the first word in each identified line of text
    fname = fn + ".json"
    return fname

def ocr_space_text_map(json_file_to_parse):
    # extracts the words in each lines and their locations and stores them in two arrays
    # eg. for a file with 20 lines of text, we have two arrays,
        # all_lines contains 20 elements, each element is a string
            # containing all the words on each line in the image
        # all_locations contains 20 elements, each element is a list [x_center_coord,y_center_coord]
            # with the location of the first word in each line (elements in both lists are paired
            # Note that locations are per image: [distance in pixels from left side, distance in pixels from top side]
    with open(json_file_to_parse, 'r+') as f:
        # read the json file
        data = json.load(f)
        # extract all the lines of text and corresponding locations of every word in each line
        line_texts_and_locs = data['ParsedResults'][0]['TextOverlay']['Lines']
        all_lines = []
        all_locations = []
        for line_text_and_loc in line_texts_and_locs:
            # for every line of text, record what the text is, in all_lines
            line_text = line_text_and_loc['LineText']
            all_lines.append(line_text)
            # for every line of text, record what the center coordinate of the first word in that line is, in all_locations
            loc_of_first_word_in_line = line_text_and_loc['Words'][0]
            x_center_coord, y_center_coord = parse_loc(loc_of_first_word_in_line)
            all_locations.append([x_center_coord, y_center_coord])
        f.close()
    return all_lines,all_locations

def ocr_request_error(json_of_ocr_result):
    # checks if there was an error in processing the image on ocr.space, such as target image file size being too large
    with open(json_of_ocr_result, 'r+') as f:
        # read the json file
        data = json.load(f)
        if data['IsErroredOnProcessing']:
            print(f"One of the requested images, with filename {json_of_ocr_result[0:len(json_of_ocr_result)-5]}, produced an error on processing by ocr.space. ")
            print(f"The error was: {data['ErrorMessage'][0]}")
            return True
    return False

def ocr_space_file_request(filename, overlay=True, api_key='0dc7f1aea588957', language='eng'):
    """ This code was found on Github, https://github.com/Zaargh/ocr.space_code_example/blob/master/ocrspace_example.py
    OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to '0dc7f1aea588957'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'eng'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()