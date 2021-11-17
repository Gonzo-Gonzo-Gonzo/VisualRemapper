#THE LENGTH OF A FRAME IS 921762 BYTES
import socket, pickle
import paramiko  
import struct

from PySimpleGUI.PySimpleGUI import Window
from torchvision.io.image import ImageReadMode
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Dataset
import tkinter as TK

import matplotlib
import os.path

import torchvision.transforms.functional as TF
from torchvision.utils import make_grid,save_image
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image, ImageTk

import cv2


import numpy as np
import time

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
    standby_image=cv2.imread('C:\\Users\\lorca\\IT masters\\Dissertation\\Program\\standby.jpg',0)
    print (type(standby_image))
    standby_image_pil=Image.fromarray(standby_image)
    
    #Device container, width is not equal to visible width. 
    devices={'HTCVive':{'width':2100,'center':1050,'height':1500}}
    #type is the type of hemianopsia the user has.
    #border_le and border_ri mark the separation of the screen, a horizontal pixel location where the border of the usersvisible field is.
    #IMPORTANT border variables are sensitive to the device they are displayed in. 
    Patient_info= {'Hemianopsia_type':'Homonymous left','border_ri':500,'border_le':1500} 
    

    def __init__(self, device, Patient_info):
        self.device=device
        self.patient_info=Patient_info
        
        if Patient_info['Hemianopsia_type'] == 'Homonymous left':
            self.right_window=TK.Tk()
            self.right_window.geometry(str(self.devices[self.device]['width']-self.Patient_info['border_ri'])+'x'+str(self.devices[self.device]['height'])+'+'+str(self.devices[self.device]['width']-self.Patient_info['border_ri'])+'+0')
            standby_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.right_img_label=TK.Label(master=self.right_window,image=standby_imtk)
            self.right_img_label.place(x=0,y=0)
            self.left_window=TK.Toplevel()
            self.left_window.geometry(str(self.patient_info['border_le']-self.devices[self.device]['center'])+'x'+str(self.devices[self.device]['height'])+'+'+str(Patient_info['border_le'])+'+0')
            standby_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.left_img_label=TK.Label(master=self.left_window,image=standby_imtk)
            self.left_img_label.place(x=0,y=0)
        elif Patient_info['Hemianopsia_type'] == 'Homonymous right':
            self.right_window=TK.Tk()
            self.right_window.geometry(str(self.patient_info['border_ri']-self.devices[device]['center'])+'x'+str(self.devices[device]['height'])+'+'+str(self.devices[device]['center'])+'+0')
            standby_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.right_img_label=TK.Label(master=self.right_window,image=standby_imtk)
            self.right_img_label.place(x=0,y=0)
            self.left_window=TK.Tk()
            self.left_window.geometry(str(self.patient_info['border_le'])+'x'+str(self.devices[device]['height']))
            standby_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.left_img_label=TK.Label(master=self.left_window,image=standby_imtk)
            self.left_img_label.place(x=0,y=0)
    def update(self, frames):
        def right_update(frame):    
            im_pil = Image.fromarray(frame)
            imTK= ImageTk.PhotoImage(im_pil)
            self.right_img_label.config(image=imTK)
            self.right_window.update()
            
        def left_update(frame):
            im_pil = Image.fromarray(frame)
            imTK= ImageTk.PhotoImage(im_pil)
            self.left_img_label.config(image=imTK)
            self.left_window.update()
        right_update(frame=frames[0])
        left_update(frame=frames[1])
    def transform (self,frame_le,frame_ri):#In go two open cv frames from cameras with 62 degrees fov, the desired frame width and the desired frame location ('center','side' or 'rigth')
        #set values for testing
        
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
        

        #Rotate the image by 270 degrees using a rotation matrix. 

        image_center = tuple(np.array(frame_le.shape[1::-1]) / 2)
        rot_matrix = cv2.getRotationMatrix2D(image_center, 270, 1.0)
        frame_le = cv2.warpAffine(frame_le, rot_matrix, frame_le.shape[1::-1], flags=cv2.INTER_LINEAR)
        print (frame_le.shape)
        frame_le=frame_le[0:639,70:440]
        print (frame_le.shape)
        frame_le=cv2.resize(src=frame_le,dsize=[int(self.left_window.winfo_width()),639])
        print (frame_le.shape)
        result.append(frame_le)
        #rotate the image by 90 degrees
        
        #do the same transformation for the right eye. 
        frame_ri= cv2.imread('c:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Test frames\\right\\10.jpeg')
        
        image_center = tuple(np.array(frame_ri.shape[1::-1]) / 2)
        rot_matrix = cv2.getRotationMatrix2D(image_center, 90, 1.0)
        frame_ri = cv2.warpAffine(frame_ri, rot_matrix, frame_ri.shape[1::-1], flags=cv2.INTER_LINEAR)
        frame_ri=frame_ri[0:639,70:440]
        frame_ri=cv2.resize(src=frame_ri,dsize=[int(self.right_window.winfo_width()),639])
        result.append(frame_ri)
        #remove the padding form the image by cutting it. 

        
        return result

def main():
    #temporary border variables. 
    Info= {'border_le':1000, 'border_ri':4000, 'Hemianopsia_type':'Homonymous_left','Headset_Type':'HTC_Vive'}

    sender_socket_ri=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sender_socket_ri.connect((right_pi_IP,2000))
    #Info = GUI0()
    sender_socket_le=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sender_socket_le.connect((Left_pi_IP,2000))
    
    
    displayer1 = displayer(Patient_info= {'Hemianopsia_type':'Homonymous left','border_ri':500,'border_le':1500},device='HTCVive')
    
    #displayer1=testDisplayer()

    

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
    

    
    while True:
        
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
        
        
        ###DONE we have both frames. 
        # Now we transfomr the frames and ipdate the display.
        frames=displayer1.transform(frame_le=frame_Le,frame_ri=frame_Ri)
        displayer1.update(frames=frames)
        print('frames updated')
        
        



if __name__=='__main__':
    main()