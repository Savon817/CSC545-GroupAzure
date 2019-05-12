import numpy as np
import cv2
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys
import threading

global video_stream
pause_video = True
current_num_fire_frames = 0
old_num_fire_frames = 0
high_confidence = False
moderate_confidence = False
low_confidence = False
fire_cascade = cv2.CascadeClassifier('myhaar.xml')
last_analysis_time = time.time()
noFireDetectedCount = 0

#select video file:
video_filename =  filedialog.askopenfilename(title = "Select video file",filetypes = (("Video files","*.mp4;*.mov;*.avi"),("All files","*.*")))
#exit if no file selected:
if not video_filename:
    messagebox.showinfo("ERROR", "No file was selected")
    exit("\nERROR: No file was selected! Exiting...")

video_stream = cv2.VideoCapture(video_filename)

def analyzeDetectionRate():
    global last_analysis_time, current_num_fire_frames, old_num_fire_frames, high_confidence, moderate_confidence, low_confidence, noFireDetectedCount

    #Analyze detection counts every 2 seconds:
    if ((time.time() - last_analysis_time) > 1.0):
        fire_frames_since_last_analysis = current_num_fire_frames - old_num_fire_frames

        if fire_frames_since_last_analysis > 12:
            #set high confidence flag:
            high_confidence = True
            moderate_confidence = False
            low_confidence = False
        elif fire_frames_since_last_analysis > 6:
            #set moderate confidence flag:
            high_confidence = False
            moderate_confidence = True
            low_confidence = False
        elif fire_frames_since_last_analysis > 1:
            #set low confidence flag:
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
        #store the current number of fire frames as the old number for later reference:
        old_num_fire_frames = current_num_fire_frames
        # record analysis time:
        last_analysis_time = time.time()


def main():

    while 1:
        if pause_video == False:
            ret, img = video_stream.read()
            current_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            global current_num_fire_frames
            analyzeDetectionRate()

            # last two parameters are detection weights:
            # first paramater is threshold for positive detection: lower means more likely to detect
            # second parameter is threshold for negative detection: higher number reduces false alarms
            # detectMultiScale(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize]]]]]) 
            fire = fire_cascade.detectMultiScale(current_frame, 1.3, 13)
                
            for (x,y,w,h) in fire:
                #Create a rectangle around the detected area:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                current_num_fire_frames += 1

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

def playVideo():
    global pause_video
    pause_video = False

def pauseVideo():
    global pause_video
    pause_video = True

def quitProgram():
    sys.exit()

def tkThread():
    r = tk.Tk()
    r.title('Fire Detection')
    exitButton = tk.Button(r, text='Exit', width=20, height=2, command=quitProgram) 
    playButton = tk.Button(r, text='Play', width=20, height=2, command=playVideo) 
    pauseButton = tk.Button(r, text='Pause', width=20, height=2, command=pauseVideo) 
    playButton.pack()
    pauseButton.pack()
    exitButton.pack()
    r.mainloop()

t1 = threading.Thread(target=main)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=tkThread).start()