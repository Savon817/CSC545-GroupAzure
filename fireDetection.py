import numpy as np
import cv2

fire_cascade = cv2.CascadeClassifier('myhaar.xml')

video_stream = cv2.VideoCapture('kitchenfire1.mp4')

while 1:
    ret, img = video_stream.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    fire = fire_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in fire:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

video_stream.release()
cv2.destroyAllWindows()