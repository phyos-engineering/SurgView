import time
import cv2 as cv
import imutils
from . import clean

#TODO: Fix single reference to self.gui_map.add_widget(button_label, center_x, center_y) -- Add Widget To Map

def contour_matching(show_results: bool, template_flag: str,template_filepath = None,source_filepath = None):
    start_time = time.time()
    if template_filepath == None:
        print("Must set a template filepath, eg. contour_matching(show_results, template_flag, template_filepath = path_to_your_target_contour,source_filepath = path_to_your_interface_to_map)")
    if source_filepath == None:
        print("Must set a source filepath, eg. contour_matching(show_results, template_flag, template_filepath = path_to_your_target_contour,source_filepath = path_to_your_interface_to_map)")
    #
    image = cv.imread(template_filepath)

    image_gray_threshold = clean(image)

    contours = cv.findContours(image_gray_threshold, cv.RETR_EXTERNAL,
                               cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    largest_cnt = max(
        contours,
        key=cv.contourArea)  # Only grab contour with largest area

    cv.drawContours(image=image,
                    contours=[largest_cnt],
                    contourIdx=0,
                    color=(0, 255, 0),
                    thickness=3)

    show_result("Contour of target image", image,
                     show_results)

    # Get Area of Contour (Important
    area = cv.contourArea(largest_cnt)

    # Load Interface Image & Make Copy:

    #interface = self.current_view
    interface = cv.imread(source_filepath)
    interface_contours = interface.copy()
    interface_result = interface.copy()

    show_result("Interface Image", interface, show_results)

    # Convert Interface Image to Grayscale
    interface_gray = cv.cvtColor(interface, cv.COLOR_BGR2GRAY)
    show_result("Interface Image After Grayscale Conversion",
                     interface_gray, show_results)

    # Apply Threshold to Grayscale Interface Image
    ret1, thresh1 = cv.threshold(interface_gray, 127, 255, 0)
    show_result("Threshold of Grayscale Image", thresh1, show_results)

    # Find Contours In Interface Image With Applied Threshold
    contours = cv.findContours(thresh1.copy(), cv.RETR_LIST,
                               cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    cv.drawContours(interface_contours,
                    contours,
                    contourIdx=-1,
                    color=(0, 255, 0),
                    thickness=3)
    show_result("Detected Contours In Interface", interface_contours,
                     show_results)

    # Establish lower and upper bound for contours areas detected in interface that match the target contour area
    lower_bound = area * 0.90
    upper_bound = area * 1.10

    # Filter for contours that fall within bounds.
    targets = []
    for i in contours:
        cnt = cv.contourArea(i)
        if lower_bound <= cnt <= upper_bound:
            targets.append(i)

    cv.drawContours(interface_result,
                    targets,
                    -1,
                    color=(0, 255, 0),
                    thickness=3)
    show_result("Target Contours", interface_result, show_results)

    # Render rects on detected objects
    rects_result = interface.copy()
    for i in targets:
        # Render a bounding rectangle for each target contour
        x, y, w, h = cv.boundingRect(i)

        # Capture region of interest within bounded rectangle (button)
        button = rects_result[y:y + h, x:x + w]
        show_result("button", button, show_results)

        # Extract name of button using OCR
        button_label = self.extract_text(button, template_flag)
        cv.rectangle(rects_result,
                     pt1=(x, y),
                     pt2=(x + w, y + h),
                     color=(0, 0, 255),
                     thickness=2)

        # Calculate & Render Center Point of Rectangle
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)

        cv.circle(rects_result, (center_x, center_y),
                  radius=2,
                  thickness=-1,
                  color=(0, 0, 255))

        # Add Widget To Map
        self.gui_map.add_widget(button_label, center_x, center_y)

    show_result("Target Area With Rects", rects_result, show_results)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Contour Matching - Elapsed Time: {}s".format(
        round(elapsed_time, 2)))

    return rects_result

def show_result(title: str, image, is_enabled: bool):
    """
    See the result of an OpenCV procedure in a new window
    :param title: Title of result window.
    :param image: The image rendered in window.
    :param is_enabled: Flag whether showing window result is enabled.
    """
    if is_enabled:
        cv.imshow(title, image)
        cv.waitKey(0)
        cv.destroyWindow(title)