#This is an old veriosn that is deprecated because if was too slow. 
#This version of sender does not use thrading.


import cv2
import pickle
import time
import socket
import struct
import Camera_reader

HOST= '192.168.1.121'
PORT= 100
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))


camera=Camera_reader.cameraStream()
camera.start()

while (True):
        print('inside while loop')
        #ret,frame=cap.read()
        #ret,frame=cap.read()
        #if ret == False:
        #       continue

        frame=camera.read()
        file_name='temporaryfile.jpeg'
        frame=cv2.imwrite(file_name,frame)
        frame=pickle.dumps(frame)
        packet = struct.pack("Q",len(frame))+frame
        s.sendall(packet)
        print ('done')

        #OLD method of splitting the data and sending it
        #n=len(frame)/10
        #for w in range (1,10):
        #       i=int(n*w)
        #       s.send(frame[0:i])
        #s.send('done')
