#THE LENGTH OF A FRAME IS 921762 BYTES
import socket, pickle
import paramiko  
import struct
import math
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
    devices={'HTCVive':{'width':2100,'center':1050,'height':1500,'left lense center':[1400,750],'right lense center':[500,750]}}
    #type is the type of hemianopsia the user has.
    #border_le and border_ri mark the separation of the screen, a horizontal pixel location where the border of the usersvisible field is.
    #IMPORTANT border variables are sensitive to the device_name they are displayed in. 
    Patient_info= {'Hemianopsia_type':'Homonymous left','border_ri':1500,'border_le':200} 
    
    def __init__(self, device_name, Patient_info, transformer):
        self.transformer=transformer
        self.device_name=device_name
        self.patient_info=Patient_info
        if Patient_info['Hemianopsia_type'] == 'Homonymous left':
            self.right_window=TK.Tk()
            #MODULATIZE
            self.right_window.geometry(str(self.devices[self.device_name]['width']-self.Patient_info['border_ri'])+'x'+str(self.devices[self.device_name]['height'])+'+'+str(self.HTC_Vive_right_lense_center)+'+0')
            self.right_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.right_img_label=TK.Label(master=self.right_window,image=self.right_imtk)
            self.right_img_label.place(x=0,y=0)
            self.left_window=TK.Toplevel()
            #MODULARIZE
            self.left_window.geometry(str(self.patient_info['border_le']-self.devices[self.device_name]['center'])+'x'+str(self.devices[self.device_name]['height'])+'+'+str(self.HTC_Vive_left_lense_center-100)+'+0')
            self.left_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.left_img_label=TK.Label(master=self.left_window,image=self.left_imtk)
            self.left_img_label.place(x=0,y=0)
        elif Patient_info['Hemianopsia_type'] == 'Homonymous right':
            self.right_window=TK.Tk()
            self.right_window.geometry(str(self.patient_info['border_ri']-self.devices[device_name]['center'])+'x'+str(self.devices[device_name]['height'])+'+'+str(self.devices[device_name]['center'])+'+0')
            self.right_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.right_img_label=TK.Label(master=self.right_window,image=self.right_imtk)
            self.right_img_label.place(x=0,y=0)
            self.left_window=TK.Tk()
            self.left_window.geometry(str(self.patient_info['border_le'])+'x'+str(self.devices[device_name]['height']))
            self.left_imtk=ImageTk.PhotoImage(self.standby_image_pil)
            self.left_img_label=TK.Label(master=self.left_window,image=self.left_imtk)
            self.left_img_label.place(x=0,y=0)
    def update(self, frames):
        def right_update(frame):    
            im_pil = Image.fromarray(frame)
            self.right_imtk= ImageTk.PhotoImage(im_pil)
            self.right_img_label.config(image=self.right_imtk)
            self.right_window.update()
            
        def left_update(frame):
            im_pil = Image.fromarray(frame)
            self.left_imtk= ImageTk.PhotoImage(im_pil)
            self.left_img_label.config(image=self.left_imtk)
            self.left_window.update()
        right_update(frame=frames[0])
        left_update(frame=frames[1])
    def process_recording(self,frame_list,fps):#fps options are 10,20,50
        reading_variable=0
        while reading_variable < len(frame_list):
            time.sleep(1/fps)
            self.update(frame_list[reading_variable])
            reading_variable+=1
        
        


#Transformer class must have a transform function that is called. 
#The attributes components must be a string containing the name of the functions that will be added to the basic transformation function.
#Every function must have a toString function that explains its purpose and the combinations it can be used in. 

class Transformer ():
    width_of_frames=639
    def __init__(self,components):
        self.components=components
    def transform (self,frame_le,frame_ri):#In go two open cv frames from cameras with 62 degrees fov, the desired frame width and the desired frame location ('center','side' or 'rigth')
        i=0
        frames = (frame_le,frame_ri)
        while i<len(self.components):
            function= 'self.transform(frames)'+self.components[i]
            frames = eval(function)
            i+=1
        return frames
    
    def transform1(frames):
        frame_le=frames[0]
        frame_ri=frames[1]
        result= [] #the list where the images will be put.    
        
        #transform the image for the left eye. 
        #Rotate the image by 270 degrees using a rotation matrix. 
        image_center = tuple(np.array(frame_le.shape[1::-1]) / 2)
        rot_matrix = cv2.getRotationMatrix2D(image_center, 270, 1.0)
        frame_le = cv2.warpAffine(frame_le, rot_matrix, frame_le.shape[1::-1], flags=cv2.INTER_LINEAR)
        print (frame_le.shape)
        #remove the padding
        frame_le=frame_le[0:639,70:440]
        print(str(self.left_window.winfo_width())+' '+str(self.left_window.winfo_height()))
        frame_le=cv2.resize(src=frame_le,dsize=[self.left_window.winfo_width(),self.left_window.winfo_height()])
        print (frame_le.shape)
        
        #rotate the image by 90 degrees
        
        #do the same transformation for the right eye. 
        
        #find center and rotate
        image_center = tuple(np.array(frame_ri.shape[1::-1]) / 2)
        rot_matrix = cv2.getRotationMatrix2D(image_center, 90, 1.0)
        frame_ri = cv2.warpAffine(frame_ri, rot_matrix, frame_ri.shape[1::-1], flags=cv2.INTER_LINEAR)
        #remove the padding
        frame_ri=frame_ri[0:639,70:440]
        #resize
        print(str(self.right_window.winfo_width())+' '+str(self.right_window.winfo_height()))
        frame_ri=cv2.resize(src=frame_ri,dsize=[self.right_window.winfo_width(),self.right_window.winfo_height()])
        print (frame_ri.shape)
            
        result.append(frame_ri)
        result.append(frame_le)
        return result
    
    def transform2_10m(self,frames):#Overlap adjuster.
        #follow the real life immitation algorithm.
        #1.Using Equation E Calculate  for human eye.
        #Calculate overlap proportion for the human eye at distance D=1000cm
        #assume a distance between eyes of 3 cm
        D=1000
        S=3
        AFOV=135
        eye_overlap= ((10*2/(math.tan((180-AFOV)/2)))-3)/(3+(10*2/(math.tan((180-AFOV)/2))))
        #calculate the overlap for the cameras with the same distance 
        D=1000
        S=2
        AFOV=70
        camera_overlap=((10*2/(math.tan((180-AFOV)/2)))-3)/(3+(10*2/(math.tan((180-AFOV)/2))))
        #Modify the frames to make the overlap more similar.
        #q is the length of the piece of frame that needs to be copied and added to the frame beside it to make the camera overlap equal the eye overlap.
        q=(eye_overlap*639-camera_overlap*639)/(1-eye_overlap)
        
        if camera_overlap<eye_overlap:
            piece0=frames[0][self.width_of_frames-q:self.width_of_frames,0:440]
            piece1=frames[1][0:q,0:440]
            #add the piece from frame 1 to frame 0 and the piece from frame 0 to frame 1.
            frames[1]=cv2.vconcat(frames[1],piece0)
            frames[0]=cv2.vconcat(frames[0],piece1)
        
            
    def increase_overlap(self, frames):
        
        piece0=frames[0][self.width_of_frames-10:self.width_of_frames,0:440]
        piece1=frames[1][0:10,0:440]
        #add the piece from frame 1 to frame 0 and the piece from frame 0 to frame 1. 
        frames[1]=cv2.vconcat(frames[1],piece0)
        frames[0]=cv2.vconcat(frames[0],piece1)
class Remapper():
    def __init__(self,Displayer,mode,Info,number_of_frames):
        self.Info=Info
        self.displayer1=Displayer
        self.number_of_frames=number_of_frames
        if mode == 'Stream':
            self.Stream()
        

    def Stream_Live(self):
       
        right_pi_IP= Info['Right_pi_IP']
        Left_pi_IP= Info['left_pi_IP']

        sender_socket_ri=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender_socket_ri.connect((right_pi_IP,2000))
        #Info = GUI0()
        sender_socket_le=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender_socket_le.connect((Left_pi_IP,2000))

        
        #The test diuslayer can be used to test that the frames are being passed on correctly. It displays them on the monitor.
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

            
            
            ###DONE we have the frame. 
            
            #Now we get the left one
            request_message=pickle.dumps('1')
            print (len(request_message))
            sender_socket_le.send(request_message)
            data_Le=b''
            while len(data_Le)<307360:
                data_Le+=conn_Le.recv(100000)
            
            try:
                frame_Ri= pickle.loads(data_Ri)
                frame_Le= pickle.loads(data_Le)
            except Exception:
                print('error with unpickling')
                continue
            
            ###DONE we have both frames. 
            # Now we transfomr the frames and ipdate the display.
            frames=self.displayer1.transform(frame_le=frame_Le,frame_ri=frame_Ri)
            self.displayer1.update(frames=frames)
            print('frames updated')

    def Stream_record(self):
        
        right_pi_IP= Info['Right_pi_IP']
        Left_pi_IP= Info['left_pi_IP']

        sender_socket_ri=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender_socket_ri.connect((right_pi_IP,2000))
        #Info = GUI0()
        sender_socket_le=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender_socket_le.connect((Left_pi_IP,2000))

        
        #The test diuslayer can be used to test that the frames are being passed on correctly. It displays them on the monitor.
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
        
        counting_variable=0
        result=[]#this list must be filled with tuples where item 0 is the left frame and item 1 is the right frame from the front facing layer. 
        while counting_variable<self.number_of_frames:
            
            request_message=pickle.dumps('1')
            print (len(request_message))
            sender_socket_ri.send(request_message)
            data_Ri=b''
            #Use recv to receive the message with the frame. 
            #There is a risk that recv returns before receiving a whole frame.This will cause 'pickle.loads' to throw a 'dta truncated exception. 
            while len(data_Ri)<307360:
                data_Ri+=conn_Ri.recv(100000) #instruct the receive method to receive something the size of a frame in bytes

            
            
            ###DONE we have the frame. 
            
            #Now we get the left one
            request_message=pickle.dumps('1')
            print (len(request_message))
            sender_socket_le.send(request_message)
            data_Le=b''
            while len(data_Le)<307360:
                data_Le+=conn_Le.recv(100000)
            
            try:
                frame_Ri= pickle.loads(data_Ri)
                frame_Le= pickle.loads(data_Le)
            except Exception:
                print('error with unpickling')
                continue
            
            ###DONE we have both frames. 
            # Now we transfomr the frames and ipdate the display.
            frames=self.displayer1.transform(frame_le=frame_Le,frame_ri=frame_Ri)
            result.append(frames)
            print('frames appended')
            counting_variable+=1
        return result


if __name__=='__main__':
    Info= {'border_le':1000, 'border_ri':4000, 'Hemianopsia_type':'Homonymous_left','Headset_Type':'HTC_Vive','left_pi_IP':'192.168.1.103','Right_pi_IP':'192.168.1.175'}
    Hypothesis= displayer(Patient_Info={'Hemianopsia_type':Info ['Hemianopsia_type'],'border_ri':Info['border_ri'],'border_le':Info['border_le'],'device_name':Info['Headset_Type']})
    Test=Remapper(Displayer=Hypothesis,mode='stream',Info=Info)
