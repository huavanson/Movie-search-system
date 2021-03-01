  
import cv2
import numpy as np
from time import perf_counter
cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


segment_count = fps*2

segment_height = int(height/segment_count)

print("segment count:", segment_count, "\n", "\nsegment_height",segment_height)
frames = []

while(cap.isOpened()):
    ret, new_frame = cap.read()
    if new_frame is None:
        break
    frames.append(new_frame)
    if len(frames) >= segment_count:    
        segments = []
        for i,frame in enumerate(frames):
            
            segments.append(frame[i*segment_height:(i+1)*segment_height])
        noodled_frame = np.concatenate(segments, axis=0)

        frames.pop(0)
        cv2.imshow('frame', noodled_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
print(a, b)   
cap.release()
cv2.destroyAllWindows()



