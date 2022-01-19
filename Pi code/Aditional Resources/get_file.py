#this script was used on the first iteration fo layer one. 

import cv2

cap= cv2.VideoCapture(0)
successful_attempts= 0

while cap.isOpened():
    for i in range (1,100):
        grab, frame = cap.read()
        if grab:
            successful_attempts+=1
        cv2.imwrite("/home/pi/Desktop/campCap/Frames/%d.jpeg" % i,frame)
    cap.release()
print ("extraction complete, successfull attempts:" + str(successful_attempts))

