import numpy as np
import cv2
import time

fire_frames_detected = 0
old_frames_detected_value = 0
high_confidence = False
moderate_confidence = False
low_confidence = False
fire_cascade = cv2.CascadeClassifier('myhaar.xml')
video_stream = cv2.VideoCapture('kitchenfire1.mp4')

last_analysis_time = time.time()

def analyzeDetectionRate():
    global last_analysis_time, fire_frames_detected, old_frames_detected_value, high_confidence, moderate_confidence, low_confidence

    if ((time.time() - last_analysis_time) > 1.0):
        if fire_frames_detected - old_frames_detected_value > 6:
            high_confidence = True
            moderate_confidence = False
            low_confidence = False
        elif fire_frames_detected - old_frames_detected_value > 4:
            high_confidence = False
            moderate_confidence = True
            low_confidence = False
        elif fire_frames_detected - old_frames_detected_value > 2:
            high_confidence = False
            moderate_confidence = False
            low_confidence = True
        old_frames_detected_value = fire_frames_detected
        last_analysis_time = time.time()

while 1:
    ret, img = video_stream.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # last two parameters are detection weights:
    # first paramater is threshold for positive detection: lower means more likely to detect
    # second parameter is threshold for negative detection: higher number reduces false alarms
    fire = fire_cascade.detectMultiScale(gray, 1.3, 13)
    
    for (x,y,w,h) in fire:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        fire_frames_detected += 1
        analyzeDetectionRate()

        if high_confidence:
            cv2.putText(img, "HIGH CONFIDENCE FIRE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        elif moderate_confidence:
            cv2.putText(img, "MODERATE CONFIDENCE FIRE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        elif low_confidence:
            cv2.putText(img, "LOW CONFIDENCE FIRE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

video_stream.release()
cv2.destroyAllWindows()

