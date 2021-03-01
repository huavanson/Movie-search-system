import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    # Convert the image into grayscale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the image using Gaussian Blur 
    gray_blur = cv2.GaussianBlur(gray, (17, 17),0)

    cartoon = cv2.divide(gray, gray_blur, scale=250.0)
    cv2.imshow('helo2',gray_blur)

    cv2.imshow('helo', cartoon)
    #print(gray_blur)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
