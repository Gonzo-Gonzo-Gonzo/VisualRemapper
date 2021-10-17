import socket, pickle
from os import set_inheritable
import paramiko  
import struct

from tkinter.constants import LEFT
from PySimpleGUI.PySimpleGUI import Window
from torchvision.io.image import ImageReadMode
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as T
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms.functional as TF
from torchvision.utils import make_grid,save_image
import matplotlib.pyplot as plt
import numpy as np
import random
import PIL
from PIL import Image 

import cv2



#import sdl2
#import sys 
#import sdl2.ext
import PySimpleGUI as sg

#Paramiko:Alloews us to make an "ssh client" which is an object representating a connection with an SSH  server.  

right_pi_IP='192.168.1.113'
Left_pi_IP='192.168.1.78'

HOST = "192.168.1.204" #IP of the computer that will receive the data from the Pi
PORT = 50007 #An arbitrary port
PORT2 = 50006
buffer = 4096 #The max number of bytes to be recevied per packet. Default 4096 but this is v small. Max seems to be 10000000000 before memory errors pop up.



class testDisplayer():
    
    def test_update1 (self,frame):
        cv2.imshow('window1',frame)

    def test_update2 (self,frame):
        
        cv2.imshow('window2',frame)
        

class displayer():
    #Device container, width is not equal to vivible width. 
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


def main():


    
    Info = GUI0()
    
    
    counter=0
    
    #displayer1 = displayer(Info['Headset_Type'],Info['leftLense_Border'],Info['rightLense_Border'],Info['Hemianopsia_Type'])
    
    displayer1=testDisplayer()

    ##Use paramiko to create a connection. We will be using this to run the necessary scripts on the pi's 
    RasPiLe=paramiko.SSHClient()        
    RasPiLe.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #RasPiLe.connect('192.168.1.113',port=22,username='pi',password='superpi',key_filename='C:\\Users\\lorca\\Desktop\\private key 113')
    RasPiLe.connect('192.168.1.113',port=22,username='pi',password='superpi')
    
    #RasPiRi=paramiko.SSHClient()
    #RasPiRi.set_missing_host_key_policy(paramik(o.AutoAddPolicy())
    #RasPiRi.connect('192.168.1.113',port=22,username='pi',password='superpi')

    stdin,stdout,stderr=RasPiLe.exec_command('python /home/pi/Desktop/camCap/getFile.py')


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))#Affix to local machine
    s.listen()
    conn,addr=s.accept()#accept any connection
    print (addr)
    if addr[0]== Left_pi_IP: 
        conn_Le=conn
        sLe=s
        print('le_connct')
    elif addr[0]==right_pi_IP:
        conn_Ri=conn
        sRi=s
        print('ri_connct')

    #s2 is the local socket, while conn_Le is the server socket in the left pi. 
    s2 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind((HOST, PORT2))#Affix to local machine
    s2.listen()
    conn2,addr2=s2.accept()#accept any connection
    print (addr2)
    if addr2[0]== Left_pi_IP: 
        conn_Le=conn2
        sLe=s2
        print('le_connct')
    elif addr2[0]==right_pi_IP:
        conn_Ri=conn2
        sRi=s2
        print('ri_connct')
    

    message_sect1_size=struct.calcsize('Q')#size of the initial secion of the message, which conatins the ength of the rest.
    #in tutotrials, this is names 'payload size'.
    while True:
        data_Ri=b''
        #get the frame form left pi. 
        #first we get the initial section which contains the length od the message. 
        while len(data_Ri)<message_sect1_size:
            print ('in loop Ri1')
            packet=conn_Ri.recv(4*1024)
            if not packet: break #in case this point is reached before data starts to arrive. 
            data_Ri+=packet
        
        ## Now take the first part of the message and unpack it so we can use it.
        message_sect2_size=data_Ri[:message_sect1_size]
        data_Ri = data_Ri[message_sect1_size:]
        message_sect2_size= struct.unpack("Q",message_sect2_size)[0]

        #Now we get receive the second part of the message(the frame) and decode it with pickle.
        while len(data_Ri)<message_sect2_size:
            print('in loop ri 2')
            data_Ri+=conn_Ri.recv(4*1024)
        frame_Ri=data_Ri[:message_sect2_size]
        other_data=data_Ri[message_sect2_size:]
        frame_Ri= pickle.loads(frame_Ri)
        ###DONE we have the frame. 

        #Now we get the left one

        
        data_Le=b''
        while len(data_Le)<message_sect2_size:
            print('in loop le 1')
            packet=conn_Le.recv(4*1024)
            if not packet:break
            data_Le+=packet

          ## Now take the first part of the message and unpack it so we can use it.
        message_sect2_size=data_Ri[:message_sect1_size]
        data_Le = data_Le[message_sect1_size:]
        message_sect2_size= struct.unpack("Q",message_sect2_size)[0]
        
        #Now we get receive the second part of the message(the frame) and decode it with pickle.
        
        while len(data_Le)<message_sect2_size:
            print ('in loop le 2')
            data_Le+=conn_Le.recv(4*1024)
        frame_Le=data_Le[:message_sect2_size]
        other_data=data_Le[message_sect2_size:]
        frame_Le= pickle.loads(frame_Le)
        
        ###DONE we have both frames. 
        # Now we transfomr the frames and send them.  


        #these two lines are astandin for the actural trnasformation process that is not yet developed. 
        #they merely return what they are sent!
        frame_Le=transform_Images(frame_Le)
        frame_Ri=transform_Images(frame_Ri)
        
        print('updating frames')
        
        displayer1.test_update1(frame_Le)
        displayer1.test_update2(frame_Ri)
        
        #displayer1.left_update(frame_le)
        #displayer1.right_update(frame_ri)
        
        #middle_section_method(frame_le,frame_ri)
        
   




if __name__=='__main__':
    main()