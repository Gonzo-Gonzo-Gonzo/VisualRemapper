# Use thsi script to test if the camera is working on the rapsberry pi. Dont forget to activate it on the Pi's settings.
import cv2
import numpy
cap=cv2.VideoCapture(0)

while cap.isOpened():
        (grabbed,frame)=cap.read()
        if grabbed== true:
                print(type(frame))
                frame=cv2.imread(frame)
                print(type(frame))
                cv2.imshow(winname=" ",mat=frame)

cap.release()
