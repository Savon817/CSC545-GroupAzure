import numpy as np
import cv2
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sys
import threading

global video_stream
pause_video = False
current_num_fire_frames = 0
old_num_fire_frames = 0
high_confidence = False
moderate_confidence = False
low_confidence = False
fire_cascade = cv2.CascadeClassifier('myhaar.xml')
last_analysis_time = time.time()
fire_frames_since_last_analysis = 0
noFireDetectedCount = 0
neighbors = 7

#select video file:
video_filename =  filedialog.askopenfilename(title = "Select video file",filetypes = (("Video files","*.mp4;*.mov;*.avi"),("All files","*.*")))
#exit if no file selected:
if not video_filename:
    messagebox.showinfo("ERROR", "No file was selected")
    exit("\nERROR: No file was selected! Exiting...")

video_stream = cv2.VideoCapture(video_filename)

def analyzeDetectionRate():
    global last_analysis_time, current_num_fire_frames, old_num_fire_frames, high_confidence, moderate_confidence, low_confidence
    global noFireDetectedCount, fire_frames_since_last_analysis

    #Analyze detection counts every 2 seconds:
    if ((time.time() - last_analysis_time) > 0.5):
        fire_frames_since_last_analysis = current_num_fire_frames - old_num_fire_frames
        if fire_frames_since_last_analysis > 4:
            #set high confidence flag:
            high_confidence = True
            moderate_confidence = False
            low_confidence = False
        elif fire_frames_since_last_analysis > 1:
            #set moderate confidence flag:
            high_confidence = False
            moderate_confidence = True
            low_confidence = False
        elif fire_frames_since_last_analysis > 0:
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
            global current_num_fire_frames, old_num_fire_frames, last_analysis_time
            analyzeDetectionRate()

            """ first parameter is image (frame) name
                second paramater is scale factor. For example, 1.05 means we are reducing image size by 5% in each iteration and are
                    more likely to match flames of different sizes compared to our training images. 1.01 is accurate but expensive
                    for the CPU. 
                third parameter specifies how many neighbors each candidate rectangle should have to retain it."""
            
            fire = fire_cascade.detectMultiScale(current_frame, 1.05, neighbors)
                
            for (x,y,w,h) in fire:
                #Create a rectangle around the detected area:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                current_num_fire_frames += 1

            
            frames_per_second = str(2 * fire_frames_since_last_analysis)
            cv2.putText(img, frames_per_second + " flame detections/sec", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (76, 255, 255), 1, lineType=cv2.LINE_AA)

            if high_confidence:
                cv2.putText(img, "HIGH CONFIDENCE FIRE", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (76, 255, 255), 1, lineType=cv2.LINE_AA)
            elif moderate_confidence:
                cv2.putText(img, "MODERATE CONFIDENCE FIRE", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (76, 255, 255), 1, lineType=cv2.LINE_AA)
            elif low_confidence:
                cv2.putText(img, "LOW CONFIDENCE FIRE", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (76, 255, 255), 1, lineType=cv2.LINE_AA)

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

def increaseNeighbors():
    global neighbors
    neighbors += 1
    print("Requiring", neighbors, "neighbors")

def decreaseNeighbors():
    global neighbors
    neighbors -= 1
    print("Requiring", neighbors, "neighbors")

def quitProgram():
    sys.exit()

def tkThread():
    r = tk.Tk()
    r.title('Fire Detection')
    exitButton = tk.Button(r, text='Exit', width=20, height=2, command=quitProgram) 
    playButton = tk.Button(r, text='Play', width=20, height=2, command=playVideo) 
    pauseButton = tk.Button(r, text='Pause', width=20, height=2, command=pauseVideo)
    increaseNeighborsButton = tk.Button(r, text='Neighbors +', width=20, height=2, command=increaseNeighbors)
    decreaseNeighborsButton = tk.Button(r, text='Neighbors -', width=20, height=2, command=decreaseNeighbors)
    playButton.pack()
    pauseButton.pack()
    increaseNeighborsButton.pack()
    decreaseNeighborsButton.pack()
    exitButton.pack()
    r.mainloop()

t1 = threading.Thread(target=main)
t1.daemon = True
t1.start()

t2 = threading.Thread(target=tkThread).start()