import cv2
import numpy as np
import math

def distotion(image):
    (h,w,c) = image.shape
    map_x = np.zeros((h,w),np.float32)
    map_y = np.zeros((h,w),np.float32)

    
    for y in range(h):
        for x in range(w):
            map_x[y,x] = x + int(20.0 * math.sin(2 * 3.14 * x / 150))
            map_y[y,x] = y + int(20.0 * math.cos(2 * 3.14 * y / 150))

   
    final = cv2.remap(image,map_x,map_y,cv2.INTER_LINEAR)
    return final 


cap = cv2.VideoCapture(0)
while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('src',frame)
    dis = distotion(frame)
    cv2.imshow ("img", dis)
    #cv2.imshow ("ori", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
