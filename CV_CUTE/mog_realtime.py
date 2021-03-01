import numpy as np
import cv2
import time


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
preframe = frame 
first = 1
while True:
    ret, frame = cap.read()
    #frame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (3,3), 0)
    if (first % 2 == 1):
        preframe = frame 
    elif (first % 2 == 0):
        difference = cv2.absdiff(frame, preframe)
        
        _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        
        
        preframe = frame
        #first = 0
    if first>1:
        cv2.imshow('helo',difference)
    first+=1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
