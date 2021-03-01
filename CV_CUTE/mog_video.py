import numpy as np
import cv2
import time

cap = cv2.VideoCapture("video-1609550054.mp4")
#cap = cv2.VideoCapture(0)
fps = 30
start_time = time.time()
queue = []
cc =[]
first = 1
difference = 0
count = 0
ngu = False
while(cap.isOpened()):
    ret, frame = cap.read()
    if (first == 1):
        preframe = frame 
    elif (first % 2 == 0):
        difference = cv2.absdiff(frame, preframe)
        
        _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        
        preframe = frame
        first = 0
    if (ngu == False):
        queue.append(frame)
    else:
        queue.append(difference)
##    if count == 60:
##        if ngu ==False: ngu = True
##        else: ngu = False
##        count=0
    if count == 60 and ngu == False:
        ngu = True
        count = 0
    if count == 120 and ngu == True:
        ngu = False
        count = 0
    
    count+=1
    cc.append(frame)
    first+=1
    now_time = time.time()
    if (now_time - start_time > 1/fps) :
        start_time = time.time()
        
        t = queue.pop(0)
        k = cc.pop(0)
        cv2.imshow('cac',t)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
