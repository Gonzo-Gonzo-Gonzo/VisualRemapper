from tkinter.constants import LEFT
from PySimpleGUI.PySimpleGUI import Window
from torchvision.io.image import ImageReadMode
import torchvision.transforms as T
import torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as T
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms.functional as TF
from torchvision.utils import make_grid
from torchvision.utils import save_image
import matplotlib.pyplot as plt
import numpy as np
import random
import PIL
from PIL import Image 

import cv2


import sdl2
import sys 
import sdl2.ext
import PySimpleGUI as sg

#Paramiko:Alloews us to make an "ssh client" which is an object representating a connection with an SSH  server.  

import paramiko  
'''
Resources= sdl2.ext.Resources(__file__,"Dead aphid.jpg")

sdl2.ext.init() 

window = sdl2.ext.Window('Hellow World!',size=(640,480))
window.show()

factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
sprite= factory. from_image(Resources.get_path("Dead aphid.jpg"))

spriterenderer= factory. create_sprite_render_system(window)
spriterenderer.render(sprite) 

processor = sdl2.ext.TestEventProcessor()
processor.run(window)

'''


'''
##this is practice code for getting familiar with tensors and other pytorch concepts. 
Test_tensor=torch.rand(3,4)
print(Test_tensor)
Test_tensor_Elements_Selection=(Test_tensor[:,-1])
print(Test_tensor_Elements_Selection)



#practice code ends here. Should delete once fully familiar. 
'''


#Video_file_timestamps= torchvision.io.read_video_timestamps("C:\\Users\\lorca\\IT masters\\Dissertation\\360_video test.mp4",'sec')

#print(Video_file_timestamps)
'''
Video_file =torchvision.io.read_video("C:\\Users\\lorca\\IT masters\\Dissertation\\TestVideo.mp4",0,1,'sec')
print(Video_file[0][0][0][0][0])
tensor_image =Video_file[0][0][0][0]

print (type (Video_file[0][0][0][0][0]))

'''



def main():

    Info = GUI0()
    #Left_window=makeWindow('left',Info['leftLense_Border'],Info['Headset_Type'],Info['Hemianopsia_Type'])
    #Right_window=makeWindow('left',Info['rightLense_Border'],Info['Headset_Type'],Info['Hemianopsia_Type'])
    counter=0
    
    RasPiLe=paramiko.SSHClient()        
    RasPiLe.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #RasPiLe.connect('192.168.1.113',port=22,username='pi',password='superpi',key_filename='C:\\Users\\lorca\\Desktop\\private key 113')
    RasPiLe.connect('192.168.1.113',port=22,username='pi',password='superpi')
    
    #RasPiRi=paramiko.SSHClient()
    #RasPiRi.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #RasPiRi.connect('192.168.1.113',port=22,username='pi',password='superpi')
    
    stdin,stdout,stderr=RasPiLe.exec_command('python /home/pi/Desktop/camCap/getFile.py')
    print (type(stdout))
    output_Le=[]
    for line in stdout:
        output_Le.append(line)
    print(output_Le)
    output_Le__=stdout.readline()
    print (type(output_Le__))
    error_Le=stderr.readline()
    print(output_Le__)
    print(error_Le)
    
    #loop through this to create the stream 
    #while(True):
    for i in range(1,3):
        ##get frame from left side pi
        stdin,stdout,stderr=RasPiLe.exec_command('Desktop/getFile.py')
        output_Le=stdout.readline()
        print(output_Le)
        ##get frame from right side pi
        #stdin,stdout,stderr=RasPiRi.exec_command('Desktop/getFile.py')
        #output_Ri=stdout.readline()
        #print(output_Ri)
        ##send opnCV tensor (as  a string) to be tranformed into a pytorch tensor and displayed.
        #Transform_and_render(left=output_le,right=output_ri)

   
   
    #    Left_window['Frame'].update()
    #    Right_window['Frame'].update()

    #Right_window.close()
    #Left_window.close()
    
    '''
    PIL_image=Image.open("C:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Dead aphid.jpg")
    

    image= torchvision.io.read_image("C:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Dead aphid.jpg",ImageReadMode.UNCHANGED)
    

    image= TF.resize(image,(400,400))
   

    PIL_image=TF.resize(PIL_image,(400,400))
   '''

#set up pathway from the raspberry pie
            


#Store the dimensions of the different size objects. 

Sizes={'HTC_vive':(1080 , 1200)}
def getHeight(headset):
    return Sizes[headset][0]
def getWidth(headset):
    return Sizes[headset][1]
    
##Program starts by calling this GUI where the user chooses a user profile to load a previously measured FOV** limits or start the program that measures it. 
#Also asks to declare the tipe of device.
def GUI0():
    #add simple GUI that allows profile choosing 

    #GUI here

    #add Tkinter GUI that allows the measurement of FOV.

    # 

    #GUI here
     
    #  
    DICT= {}
    DICT['Headset_Type']='HTC_vive'
    DICT['rightLense_Border']=600
    DICT['leftLense_Border']=600
    DICT['Hemianopsia_Type']='homonymous_left'
    return DICT

##Get input. Start the cameras or connect to the source. 


### Part of the program that transformas and displays the images



sample_border=500 
def RasPi_Frame_Transform(image1,image2):

    image1_central=TF.crop


def makeWindow(lense,border,headset_type,Hemianopsia_type):
    PIL_image=Image.open("C:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Dead aphid.jpg")
    layout= [[sg.InputText(key='Tests')]]
    #layout= [[sg.Image("C:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Dead aphid.jpg",key='Frame')]]
    height=getHeight(headset_type)
    width=''
    location=''
    if Hemianopsia_type=='homonymous_right':
        if  lense=='left':
            location=(0,0)
            width=border
        elif lense=='right':
            location=(0,0)
            width=border
    elif Hemianopsia_type== 'homonymous_left':
        if  lense=='left':
            location=(0,border)
            width=getWidth(headset_type)-border
        elif lense=='right':
            location=(0,border)
    Window_identifier= lense+' lense window'
    return sg.Window(Window_identifier,no_titlebar=True,layout=layout,location=location,size=(height,width))    



##starting with a large 2:1 image. Make a copy. Crop and then resize to produce the images of each lense. 
# the resizing and rechaping should be done according to two values representing the beguining of the users unsusable FOV in each eye. 
'''
PIL_image=Image.open("C:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Dead aphid.jpg")
PIL_image.show()
print(PIL_image)

image= torchvision.io.read_image("C:\\Users\\lorca\\IT masters\\Dissertation\\Program\\Dead aphid.jpg",ImageReadMode.UNCHANGED)
print(image.size())

image= TF.resize(image,(400,400))
print(image.size())

PIL_image=TF.resize(PIL_image,(400,400))
PIL_image.show()
'''
##Now create two windows in the correct area of each lense





if __name__=='__main__':
    main()