#THE LENGTH OF A FRAME IS 921762 BYTES
import socket, pickle
import paramiko  
import struct

from PySimpleGUI.PySimpleGUI import Window
from torchvision.io.image import ImageReadMode
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Dataset

import matplotlib
import os.path

import torchvision.transforms.functional as TF
from torchvision.utils import make_grid,save_image
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image 

import cv2



#import sdl2
#import sys 
#import sdl2.ext
import PySimpleGUI as sg

#Paramiko:Alloews us to make an "ssh client" which is an object representating a connection with an SSH  server.  

right_pi_IP='192.168.1.175'
Left_pi_IP='192.168.1.103'

HOST = "192.168.1.121" #IP of the computer that will receive the data from the Pi
PORT = 107 #An arbitrary port
PORT2 = 105
buffer = 4096 #Deprecated and not used in alternate version The max number of bytes to be recevied per packet. Default 4096 but this is v small. Max seems to be 10000000000 before memory errors pop up.



class testDisplayer():
    
    def test_update1 (self,frame):
        cv2.imshow('window1',frame)
        cv2.waitKey(1)

    def test_update2 (self,frame):
        
        cv2.imshow('window2',frame)
        cv2.waitKey(1)

    def transform_frame(self,frame):
        return frame
        

class displayer():
    #Device container, width is not equal to visible width. 
    devices={'HTCVive':{'width':2100,'center':1050,'height':1500}}
    #type is the type of hemianopsia the user has.
    #Border_le and Border_ri mark the separation of the screen in pixels. 
    

    def __init__(self,device,Border_le,Border_ri,type):
        self.device=device
        layout=[[sg.Image(key='Image')]]
        layout2=[[sg.Image(key='Image')]]
        if type == 'Homonimous left':
            self.right_window=sg.Window('right',no_titlebar=True,layout=layout,location=Border_ri,size=(self.devices[device]['width']-Border_ri,self.devices[device]['height']))
            self.left_window=sg.Window('left',no_titlebar=True,layout=layout2,location=Border_le,size=(self.devices[device]['center']-Border_le,self.devices[device]['height']))
        elif type == 'Homonymous right':
            self.right_window= sg.Window('right',no_titlebar=True,layout=layout,location=self.devices[device]['center'],size=(self.devices[device]['center'],self.devices[device]['center']))
            self.left_window=sg.Window('right',no_titlebar=True,layout=layout2,location=0,size=(Border_le,self.devices[device]['width']))
    def right_update(self,imgTensor):
        #Transform1=T.ToPILImage()
        #Image=Transform1(imgTensor)
        im_pil = Image.fromarray(imgTensor)
        self.right_window['Image'].update(Image)
    def left_update(self, imgTensor):
        #Transform1=T.ToPILImage()
        #Image=Transform1(imgTensor)
        im_pil = Image.fromarray(imgTensor)
        self.left_window['Image'].update(Image)


def main_test():
    transform('','','','')

def main():


    sender_socket_ri=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sender_socket_ri.connect((right_pi_IP,2000))
    #Info = GUI0()
    sender_socket_le=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sender_socket_le.connect((Left_pi_IP,2000))
    
    counter=0
    
    #displayer1 = displayer(Info['Headset_Type'],Info['leftLense_Border'],Info['rightLense_Border'],Info['Hemianopsia_Type'])
    
    displayer1=testDisplayer()
    print ('1')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))#Affix to local machine
    s.listen()
    print('listening')
    conn,addr=s.accept()#accept any connection
    print (addr)
    if addr[0]== Left_pi_IP: 
        conn_Le=conn
        sLe=s #listening socket, dont use 
        print('le_connct')
    elif addr[0]==right_pi_IP:
        conn_Ri=conn
        sRi=s#listening socket, dont use
        print('ri_connct')

    #s2 is the local socket, while conn_Le is the server socket in the left pi. 
    s2 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind((HOST, PORT2))#Affix to local machine
    s2.listen()
    conn2,addr2=s2.accept()#accept any connection
    print (addr2)
    if addr2[0]== Left_pi_IP: 
        conn_Le=conn2
        sLe=s2#listening socket, dont use
        print('le_connct')
    elif addr2[0]==right_pi_IP:
        conn_Ri=conn2
        sRi=s2#listening socket, dont use
        print('ri_connct')
    

    message_sect1_size=struct.calcsize('Q')#size of the initial secion of the message, which conatins the ength of the rest.
    #in tutotrials, this is names 'payload size'.
    while True:
        '''
        data_Ri=b''
        #get the frame form left pi. 
        #first we get the initial section which contains the length od the message. 
        while len(data_Ri)<message_sect1_size:
            print ('in loop Ri1')
            packet=conn_Ri.recv(32*1024)
            if not packet: break #in case this point is reached before data starts to arrive. 
            data_Ri+=packet
        
        ## Now take the first part of the message and unpack it so we can use it.
        #Remember, section 1 of the message is the length of section 2 of the message. 
        message_sect2_size=data_Ri[:message_sect1_size]
        #data_Ri = data_Ri[message_sect1_size:]
        message_sect2_size= struct.unpack("Q",message_sect2_size)[0]
        '''
        request_message=pickle.dumps('1')
        print (len(request_message))
        sender_socket_ri.send(request_message)
        data_Ri=b''
        #Use recv to receive the message with the frame. 
        #There is a risk that recv returns before receiving a whole frame.This will cause 'pickle.loads' to throw a 'dta truncated exception. 
        while len(data_Ri)<307360:
            data_Ri+=conn_Ri.recv(100000) #instruct the receive method to receive something the size of a frame in bytes

        try:
            frame_Ri= pickle.loads(data_Ri)
        except Exception:
            print('error with unpickling')
        
        ###DONE we have the frame. 
        displayer1.test_update1(frame_Ri)
        #Now we get the left one
        request_message=pickle.dumps('1')
        print (len(request_message))
        sender_socket_le.send(request_message)
        data_Le=b''
        while len(data_Le)<307360:
            data_Le+=conn_Le.recv(100000)
        
        try:
            frame_Le= pickle.loads(data_Le)
        except:
            print('error with unpickling')
        
        
        displayer1.test_update2(frame_Ri)
        ###DONE we have both frames. 
        # Now we transfomr the frames and send them.  
        print (frame_Le)
        print(frame_Ri)

        #these two lines are a standin for the actual trnasformation process that is not yet developed. 
        #they merely return what they are sent!
        #frame_Le=displayer1.transform_frame(frame_Le)
        #frame_Ri=displayer1.transform_frame(frame_Ri)
        
        print('updating frames')
        
        
        displayer1.test_update2(frame_Ri)
        
        #displayer1.left_update(frame_le)
        #displayer1.right_update(frame_ri)
        
        #middle_section_method(frame_le,frame_ri)
        
import numpy as np
import time
#Outputs two frames, which are then shown to the user in the vr.
#it needs to be adaptable so we can change (i) the size of the output frames and (ii) the location within the VR lense of the frames.
def transform (frame_le,frame_ri,width_le,width_ri):#In go two open cv frames from cameras with 62 degrees fov, the desired frame width and the desired frame location ('center','side' or 'rigth')
    #set values for testing
    width_le=200
    width_ri=200
    
    result= [] #the list whene the images will be put.    
    '''
    cap=cv2.VideoCapture(0)
    i=0
    while i in range (1,2):
        print('-')
        ret, frame=cap.read()
        print (frame)
        print (frame.shape)
        print (ret)
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
    cap.release()

    
    '''
    #transform the image for the left eye. 
    frame_le= cv2.imread('c:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Test frames\\left\\10.jpeg')
    

    #Rotate the image by 270 degrees using a rotation matrix. 

    image_center = tuple(np.array(frame_le.shape[1::-1]) / 2)
    rot_matrix = cv2.getRotationMatrix2D(image_center, 270, 1.0)
    frame_le = cv2.warpAffine(frame_le, rot_matrix, frame_le.shape[1::-1], flags=cv2.INTER_LINEAR)
    print (frame_le.shape)
    frame_le=frame_le[0:639,70:440]
    print (frame_le.shape)
    frame_le=cv2.resize(src=frame_le,dsize=[int(width_le),639])
    print (frame_le.shape)
    result.append(frame_le)
    #rotate the image by 90 degrees
    
    #do the same transformation for the right eye. 
    frame_ri= cv2.imread('c:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Test frames\\right\\10.jpeg')
    
    image_center = tuple(np.array(frame_ri.shape[1::-1]) / 2)
    rot_matrix = cv2.getRotationMatrix2D(image_center, 90, 1.0)
    frame_ri = cv2.warpAffine(frame_ri, rot_matrix, frame_ri.shape[1::-1], flags=cv2.INTER_LINEAR)
    frame_ri=frame_ri[0:639,70:440]
    frame_ri=cv2.resize(src=frame_ri,dsize=[int(width_ri),639])
    result.append(frame_ri)
    #remove the padding form the image by cutting it. 

    
    return result

    

    


    
    while range(1,100):
        cv2.imshow('frame_ri',frame_le)
        cv2.imshow ('frame ri',frame_ri)
        cv2.waitKey(1)


   
 
    



if __name__=='__main__':
    main()