import time
import os
import requests

def ocr_space_matching(self):
    """
            Search for widget in interface using ocr, which identifies bounding boxes for text
    """
    directory = 'interface_assets/steris/home_page_root_templates/'
    num_images = 0
    start_time = time.time()
    for fn in os.listdir(directory):
        if fn.endswith(".jpg") or fn.endswith(".png"):
            # opens home page root templates and saves a json of the ocr_space result
            num_images += 1
            parsed_result = ocr_space_file_request(filename=fn)
            jsonFile = open(fn + ".json", "w")
            jsonFile.write(parsed_result)
            jsonFile.close()
            #TODO: get coordinates of rectangle for each text element in the image in a format compatible with mapping.py
        else:
            continue
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"{num_images} different images were parsed using ocr.space. It took {round(elapsed_time, 1)} seconds, or {round(elapsed_time / num_images, 1)} seconds each.")


def ocr_space_file_request(filename, overlay=False, api_key='0dc7f1aea588957', language='eng'):
    """ OCR.space API request with local file.
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