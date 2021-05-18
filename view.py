# !/usr/bin/env python
# title           :view.py
# description     :Interface Mapping Class using OpenCV
# author          :Juan Maldonado
# date            :5/11/2021
# version         :0.0
# usage           :SEE README.md
# python_version  :3.7.10
# conda_version   :4.9.2
# ========================================================================================================

from mapping import ScreenMap
import cv2 as cv
import pytesseract
import numpy as np
import time
import os
import argparse
import imutils

"""
The UIReader class helps map out the screen locations of interface widgets using OpenCV.
"""


class UIReader:
	def __init__(self):
		"""
		Constructor. Initializes video feed and configures appropriate directories (tentative).
		"""
		self.program_name = None  # To Do: Exception Handling
		self.page_name = None  # To Do: Exception Handling
		self.assets_directory = "/interface_assets/"  # Directory location of templates.
		self.gui_map = ScreenMap()  # Class of charge of tracking widgets identified by UIReader.
		self.capture_feed = cv.VideoCapture(0)  # Device (USB Capture Card) outputting video feed of program.
		self.source_filepath = None
		self.template_filepath = None

	def read_video_feed(self):
		"""
		Read one frame from the video feed (USB Capture Card) and write to file.
		"""
		ret, frame = self.capture_feed.read()
		cv.imshow("test?", frame)
		cv.waitKey(0)
		cv.imwrite("current_view.png", frame)

	def test_video_feed(self):
		"""
		Test video feed.
		"""
		if not self.capture_feed.isOpened():
			print("Cannot open camera")
			exit()

		while True:
			ret, frame = self.capture_feed.read()
			if not ret:
				break

			cv.imshow('Frame', frame)
			if cv.waitKey(1) == ord('q'):
				break
		self.capture_feed.release()
		cv.destroyAllWindows()

	def extract_text(self, extracted_image) -> str:  # TO DO: Pass filepath or mat?
		"""
		Extract text from an image using Google Tesseract.
		"""
		start_time = time.time()
		img_gray = cv.cvtColor(extracted_image, cv.COLOR_BGR2GRAY)
		ret, threshold = cv.threshold(img_gray, 127, 255, 0)
		extracted_text = pytesseract.image_to_string(image=threshold.copy(), lang='eng',
													 config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
		cleaned_text = ''.join(e for e in extracted_text if e.isalnum()).lower()
		end_time = time.time()
		elapsed_time = end_time - start_time
		print("Extracting Text: {} - Elapsed Time: {}s".format(cleaned_text, round(elapsed_time, 2)))
		return cleaned_text

	def select_mapping_method(self, flag: str, show_steps: bool):
		"""
		Selects mapping method
		:param flag: Mapping method name. Options -> [TEMPLATE_MATCHING, FEATURE_MATCHING]
		:param show_steps: Display windows showing image transformations. True->Show, False-> Don't Show
		"""
		if flag == "TEMPLATE_MATCHING":
			self.template_matching()

		if flag == "FEATURE_MATCHING":
			print("Not implemented yet")

		if flag == "CONTOUR_MATCHING":
			self.contour_matching(show_steps)
		else:
			print("Mapping Method Provided Not Found")

	def show_result(self, title: str, image, is_enabled: bool):
		"""
		See the result of an OpenCV procedure in a new window
		:param title:
		:param image:
		:param is_enabled:
		"""
		if is_enabled:
			cv.imshow(title, image)
			cv.waitKey(0)
			cv.destroyWindow(title)

	def contour_matching(self, show_results: bool):
		start_time = time.time()

		image = cv.imread(self.template_filepath)
		# Read Image
		self.show_result("Target image", image, show_results)
		target_result = image.copy()

		# Covert to Grayscale
		image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

		self.show_result("Target Image In Grayscale", image_gray, show_results)

		# Apply Threshold
		ret, threshold = cv.threshold(image_gray, 127, 255, 0)
		self.show_result("Grayscale image with a threshold applied", threshold, show_results)

		# Find Contours Of Target Image
		contours = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		contours = contours[0] if len(contours) == 2 else contours[1]

		largest_cnt = max(contours, key=cv.contourArea)  # Only grab contour with largest area

		cv.drawContours(image=target_result, contours=[largest_cnt], contourIdx=0, color=(0, 255, 0), thickness=3)

		self.show_result("Contour of target image", target_result, show_results)

		# Get Area of Contour (Important
		area = cv.contourArea(largest_cnt)

		# Get Dimensions
		x, y, w, h = cv.boundingRect(largest_cnt)

		# Load Interface Image & Make Copy

		interface = cv.imread(self.source_filepath)
		interface_contours = interface.copy()
		interface_result = interface.copy()

		self.show_result("Interface Image", interface, show_results)

		# Convert Interface Image to Grayscale
		interface_gray = cv.cvtColor(interface, cv.COLOR_BGR2GRAY)
		self.show_result("Interface Image After Grayscale Conversion", interface_gray, show_results)

		# Apply Threshold to Grayscale Interface Image
		ret1, thresh1 = cv.threshold(interface_gray, 127, 255, 0)
		self.show_result("Threshold of Grayscale Image", thresh1, show_results)

		# Find Contours In Interface Image With Applied Threshold
		contours = cv.findContours(thresh1.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)
		cv.drawContours(interface_contours, contours, contourIdx=-1, color=(0, 255, 0), thickness=3)
		self.show_result("Detected Contours In Interface", interface_contours, show_results)

		# Establish a lower and upper bound for contours areas detected in interface that match the target contour area
		lower_bound = area * 0.90
		upper_bound = area * 1.10

		# Filter for contours that fall within bounds.
		targets = []
		for i in contours:
			cnt = cv.contourArea(i)
			if lower_bound <= cnt <= upper_bound:
				targets.append(i)

		cv.drawContours(interface_result, targets, -1, color=(0, 255, 0), thickness=3)
		self.show_result("Target Contours", interface_result, show_results)

		# Render rects on detected objects
		rects_result = interface.copy()
		for i in targets:
			# Render a bounding rectangle for each target contour
			x, y, w, h = cv.boundingRect(i)

			# Capture region of interest within bounded rectangle (name of button)
			button = rects_result[y:y + h, x:x + w]
			self.show_result("button", button, show_results)

			# Extract name of button using OCR
			button_label = self.extract_text(button)
			cv.rectangle(rects_result, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)

			# Calculate & Render Center Point of Rectangle
			center_x = int(x + w / 2)
			center_y = int(y + h / 2)

			cv.circle(rects_result, (center_x, center_y), radius=2, thickness=-1, color=(0, 0, 255))

			# Add Widget To Map
			self.gui_map.add_widget(button_label, center_x, center_y)

		self.show_result("Target Area With Rects", rects_result, show_results)
		end_time = time.time()
		elapsed_time = end_time - start_time
		print("Contour Matching - Elapsed Time: {}s".format(round(elapsed_time, 2)))

	def map_interface(self):
		print("Mapping Interface...")

	def template_matching(self):
		"""
		Search for widget in interface using template matching
		"""

		# Run template matching over entire dataset of assets
		start_time = time.time()
		image_dir = "interface_assets/steris/home_page/"  # TO DO: Temp make this dynamic
		interface_img = cv.imread(self.source_filepath)  # TO DO: Put this file somewhere else in the future.
		result = interface_img.copy()

		for image in os.listdir(image_dir):
			relative_path = os.path.join(image_dir, image)
			print("Finding: {}".format(image))
			widget_img = cv.imread(relative_path)

			# Convert template image to Grayscale Coloring and it's threshold to binary

			partial_image = cv.cvtColor(widget_img, cv.COLOR_RGB2GRAY)
			partial_image = cv.threshold(partial_image, 0, 255, cv.THRESH_BINARY)[1]

			# Get contour from partial image
			contours = cv.findContours(partial_image.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
			contours = contours[0] if len(contours) == 2 else contours[1]
			# Grab largest contour
			big_contours = max(contours, key=cv.contourArea)

			# Build mask based off contour
			mask = np.zeros((widget_img.shape[0], widget_img.shape[1], 3), dtype=np.uint8)
			cv.drawContours(mask, [big_contours], 0, (255, 255, 255), 1)

			# Capture height and width of mask (necessary to bound detection boxes).
			hh, ww = mask.shape[:2]

			# Extract template from BGR image
			template = widget_img[:, :, 0:3]

			# Perform Template Matching With A Mask Applied
			correlation = cv.matchTemplate(image=interface_img, templ=template, method=cv.TM_CCORR_NORMED,
										   mask=mask)
			min_val, max_val, min_loc, max_loc = cv.minMaxLoc(src=correlation)

			# Get coordinates of area in source that matched with template
			xx = max_loc[0]
			yy = max_loc[1]

			# Draw template bounds

			cv.rectangle(img=result, pt1=(xx, yy), pt2=(xx + ww, yy + hh), color=(0, 0, 255), thickness=1)

		# Show results
		end_time = time.time()
		elapsed_timed = end_time - start_time
		print("Elapsed Time: {}s".format(elapsed_timed))
		print("Average Processing Time Per Template: {}s".format(elapsed_timed / len(os.listdir(image_dir))))

		cv.waitKey(0)


def main():
	ap = argparse.ArgumentParser(description="Test Mapping Methods.")
	ap.add_argument("--map_method", nargs='?', default="CONTOUR_MATCHING", type=str,
					choices=["TEMPLATE_MATCHING", "FEATURE_MATCHING", "CONTOUR_MATCHING"],
					help="Mapping method applied to locate widgets.")
	ap.add_argument("--source", nargs='?', default="home_page_root.jpg", type=str,
					help="Source image where mapping will be performed.")
	ap.add_argument("--template", nargs='?', default="vitals_camera.jpg",
					help="Template that will be searched in source image.", type=str)
	ap.add_argument("--steps", nargs='?', default=0, type=bool, help="Display image transformations on screen.")
	args = vars(ap.parse_args())

	viewer = UIReader()
	viewer.source_filepath = args["source"]
	viewer.template_filepath = args["template"]
	viewer.select_mapping_method(args["map_method"], args["steps"])
	viewer.gui_map.get_map()


if __name__ == "__main__":
	main()
