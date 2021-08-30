# title           :ocr_space_matching.py
# description     :uses ocr.space to map widgets on a given source interface
# author          :Dan Fu
# last modified   :08/29/2021
# version         :0.0
# usage           :see below
# python_version  :3.7.10
# conda_version   :4.9.2
# ========================================================================================================

import time
import os
from . import view
from .ocr_space_methods import ocr_space_file_request,make_beautified_json,ocr_request_error,ocr_space_text_map

"""
Identify all lines of text in the image and assigns a location for each
"""

def ocr_space_matching(showResults = False):
    """
    Identify all lines of text in the image and assigns a location for each
    """
    #TODO:
    # address edge cases where buttons that span two lines like Volume Up and Volume Down are represented as two buttons
    # (maybe if there are two identical lines, remove them both instead of adding to the gui map)
    # add cleaning for each file before it is sent to ocr.space to avoid image exceeding size limit
    # also can potentially add a source_filepath or source_directory input parameter so the directory can be changed
    # (reluctant to do so before refactoring other matching algorithms, which use a source_filepath, not source_directory)
    # (once tested sufficeintly, will likely change this to source_filepath)

    directory = '../interface_assets/steris/home_page_root_templates/'
    num_images = 0
    start_time = time.time()
    for fn in os.listdir(directory):
        if fn.endswith(".jpg") or fn.endswith(".png"):
            # opens each home page root template and requests ocr.space processing
            num_images += 1
            fname = directory + fn
            ocr_result = ocr_space_file_request(filename=fname)
            json_of_ocr_result = make_beautified_json(ocr_result, target_image_filename=fname)
            if (ocr_request_error(json_of_ocr_result)):
                pass
                # if there was an error in processing the file, skip that image and print an error message
            else: # otherwise if the image was successfuly parsed by ocr.space, return all the words and their locations
                all_lines,all_locations = ocr_space_text_map(json_file_to_parse=json_of_ocr_result)
                if showResults:
                    print(f'The image {fn} was correctly parsed with outputs below:')
                    print(f'  All lines of text: {all_lines}')
                    print(f'  All locations of text: {all_locations}')
            #TODO: make coordinates of rectangle for each text element in the image compatible with mapping.py
            # this will involve a refactoring of map_interface to be more generic (not just specific to contour_matching, see view.py)
            # ADDING WIDGET NEEDS TO HAPPEN OUTSIDE OF THIS METHOD
            #reader = view.UIReader()
            #reader.gui_map.add_widget(button_label, center_x, center_y)
        else:
            continue
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"\n {num_images} different images were parsed using ocr.space. It took {round(elapsed_time, 1)} seconds, or {round(elapsed_time / num_images, 1)} seconds each.")
    return 0 # if the image/s were successfully processed, return 0 indicating success

ocr_space_matching(showResults=True)