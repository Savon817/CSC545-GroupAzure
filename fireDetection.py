import numpy as np
import cv2
import time
import tkinter as tk
import sys
import threading

global video_stream
fire_frames_detected = 0
old_frames_detected_value = 0
high_confidence = False
moderate_confidence = False
low_confidence = False
fire_cascade = cv2.CascadeClassifier('myhaar.xml')
video_stream = cv2.VideoCapture('kitchenfire1.mp4')
last_analysis_time = time.time()
noFireDetectedCount = 0


def analyzeDetectionRate():
    global last_analysis_time, fire_frames_detected, old_frames_detected_value, high_confidence, moderate_confidence, low_confidence, noFireDetectedCount

    #Analyze detection counts every 2 seconds:
    if ((time.time() - last_analysis_time) > 2.0):
        if fire_frames_detected - old_frames_detected_value > 24:
            high_confidence = True
            moderate_confidence = False
            low_confidence = False
        elif fire_frames_detected - old_frames_detected_value > 12:
            high_confidence = False
            moderate_confidence = True
            low_confidence = False
        elif fire_frames_detected - old_frames_detected_value > 1:
            high_confidence = False
            moderate_confidence = False
            low_confidence = True
        else:
            #If no fire frames are detected after several repetitions, clear the warning:
            noFireDetectedCount += 1
            if noFireDetectedCount > 2:
                high_confidence = False
                moderate_confidence = False
                low_confidence = False
                noFireDetectedCount = 0
        old_frames_detected_value = fire_frames_detected
        last_analysis_time = time.time()


def main():

    while 1:
        ret, img = video_stream.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        global fire_frames_detected
        analyzeDetectionRate()

        # last two parameters are detection weights:
        # first paramater is threshold for positive detection: lower means more likely to detect
        # second parameter is threshold for negative detection: higher number reduces false alarms
        fire = fire_cascade.detectMultiScale(gray, 1.3, 13)
            
        for (x,y,w,h) in fire:
            #Create a rectangle around the detected area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            fire_frames_detected += 1

        if high_confidence:
            cv2.putText(img, "HIGH CONFIDENCE FIRE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (76, 255, 255), 2, lineType=cv2.LINE_AA)
        elif moderate_confidence:
            cv2.putText(img, "MODERATE CONFIDENCE FIRE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (76, 255, 255), 2, lineType=cv2.LINE_AA)
        elif low_confidence:
            cv2.putText(img, "LOW CONFIDENCE FIRE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (76, 255, 255), 2, lineType=cv2.LINE_AA)

        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

def quitProgram():
    sys.exit()

def tkThread():
    r = tk.Tk()
    r.title('Fire Detection')
    exitButton = tk.Button(r, text='Exit', width=15, height=1, command=quitProgram) 
    playButton = tk.Button(r, text='Play', width=15, height=1, command=playVideo) 
    pauseButton = tk.Button(r, text='Pause', width=15, height=1, command=pauseVideo) 
    selectVideoButton = tk.Button(r, text='Select Video', width=15, height=1, command=selectVideo) 
    selectVideoButton.pack()
    playButton.pack()
    pauseButton.pack()
    exitButton.pack()
    r.mainloop()

t1 = threading.Thread(target=main)
t1.daemon = True

t2 = threading.Thread(target=tkThread).start()