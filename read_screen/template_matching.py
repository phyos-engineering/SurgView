import time
import cv2 as cv
import os
import numpy as np


def template_matching(source_filepath):
    """
    Search for widget in interface using template matching
    """
    # source_filepath = "interface_assets/steris/home_page_templates/home_page_root.jpg"
    # Run template matching over entire dataset of assets
    start_time = time.time()
    image_dir = "../interface_assets/steris/home_page_templates/"  # TO DO: Temp make this dynamic
    interface_img = cv.imread(
        source_filepath
    )  # TO DO: Put this file somewhere else in the future.
    result = interface_img.copy()

    for image in os.listdir(image_dir):
        relative_path = os.path.join(image_dir, image)
        print("Finding: {}".format(image))
        widget_img = cv.imread(relative_path)

        # Convert template image to Grayscale Coloring and it's threshold to binary

        partial_image = cv.cvtColor(widget_img, cv.COLOR_RGB2GRAY)
        partial_image = cv.threshold(partial_image, 0, 255,
                                     cv.THRESH_BINARY)[1]

        # Get contour from partial image
        contours = cv.findContours(partial_image.copy(), cv.RETR_EXTERNAL,
                                   cv.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        # Grab largest contour
        big_contours = max(contours, key=cv.contourArea)

        # Build mask based off contour
        mask = np.zeros((widget_img.shape[0], widget_img.shape[1], 3),
                        dtype=np.uint8)
        cv.drawContours(mask, [big_contours], 0, (255, 255, 255), 1)

        # Capture height and width of mask (necessary to bound detection boxes).
        hh, ww = mask.shape[:2]

        # Extract template from BGR image
        template = widget_img[:, :, 0:3]

        # Perform Template Matching With A Mask Applied
        correlation = cv.matchTemplate(image=interface_img,
                                       templ=template,
                                       method=cv.TM_CCORR_NORMED,
                                       mask=mask)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(src=correlation)

        # Get coordinates of area in source that matched with template
        xx = max_loc[0]
        yy = max_loc[1]

        # Draw template bounds

        cv.rectangle(img=result,
                     pt1=(xx, yy),
                     pt2=(xx + ww, yy + hh),
                     color=(0, 0, 255),
                     thickness=1)

    # Show results
    end_time = time.time()
    elapsed_timed = end_time - start_time
    print("Elapsed Time: {}s".format(elapsed_timed))
    print("Average Processing Time Per Template: {}s".format(
        elapsed_timed / len(os.listdir(image_dir))))

    cv.waitKey(0)