import cv2 as cv
import time
cap = cv.VideoCapture(0) 
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1920)
time.sleep(3)

if not cap.isOpened():
    print("Cannot Open Camera")
    exit()

cap.grab()
ret, frame = cap.retrieve()
cv.imshow("test?", frame)
cv.waitKey(0)




cap.release()
cv.destroyAllWindows()
exit()
