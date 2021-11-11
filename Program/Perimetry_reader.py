'''
DEBUGGING:
    Problem:windows wont render.

try changing the update methods

look for iisues in the creation of the canvases.

There might be a loop issue (loops running within loop)
there might be a problem with all the threads we are using,
try running the program without them, they may not be needed!


'''

from tkinter import Tk, Canvas, Frame, BOTH,ttk
import time
import tkinter
from tkinter.constants import W 
import winsound
import threading #deprecated

lense_info={}

width=1920 #deprecated
height=1080 #deprecated

class container():
    x_pos=0
    y_pos=0
    border_vals=[(0,0)]
    def update_xpos(self,int):
        self.x_pos=int
    def update_ypos(self,int):
        self.y_pos=int
    def Notify(self,thing):
        print (thing)
        print (self.x_pos)
        print(self.y_pos)
        self.border_vals.append((self.x_pos,self.y_pos))
        print ('notified')
    def get_and_reset (self):
        self.clean_data()
        vals=self.border_vals
        self.border_vals=[(0,0)]
        self.x_pos=0
        self.y_pos=0
        print (vals)
        return vals
    def clean_data(self):
        self.border_vals=self.border_vals[1]
       
        
class reader():
    def __init__(self, Display, Type):
        self.Display= Display  
        self.HemianopsiaType=Type
    
    def start(self):
        borders=run_test(HemianopsiaType=self.HemianopsiaType,Display=self.Display)
        return borders

#In the width and height variables of the main loop you must enter the width and the height of the VR screen. 
def run_test (HemianopsiaType='right',Display='Test'):
    
    #create the data for xpos, y pos and the blindsdpots
    data = container()
    #create the root window
    root = Tk()
    #place the window in the right place
    Screen_height=root.winfo_screenheight()-100
    Screen_width=root.winfo_screenwidth()-100
    root.geometry((str(Screen_width+20)+'x'+str(Screen_height+20)+'+0+0'))
    #create the canvas and put it on the window
    canvas=Canvas(root,width=Screen_width,height=Screen_height,bg='#fff')
    canvas.grid(row=0,rowspan=3)
    root.update()
    #create a button for notifying and put it in the root window
    btn=ttk.Button(root, text='Notify')
    #Bind it to the notify function in the data. 
    btn.bind('<Button-1>',data.Notify)
    #place the button at the bottom right 
    btn.grid(row=3,rowspan=1)
    root.update()
    
    right_can='' 
    left_can=''

    
    #realcenters need to be calculated with fov_measure of particular device. 
    
    
    
    #lense_Info contains the information necessary for arranging the canvas, button, window, etc, for each device. 
    #The storage and access of of this information could be improved, in a future version a database should be used. 
    lense_Info={'Test':{'left_lense_left':0,'left_lense_right':Screen_width/2,'right_lense_left':Screen_width/2,'right_lense_right':Screen_width,'right_lense_center':[3*Screen_width/4,Screen_height/2],'left_lense_center':[Screen_width/4,Screen_height/2]},'HTC_Vive':{'left_lense_left':250,'left_lense_right':900,'right_lense_left':1100,'right_lense_right':1800}}
    
    
    lense_Info=lense_Info[Display]

    right_border = ''
    left_border = ''
    

    if HemianopsiaType=='left':
        
        #do the left eye
        left_border=Oval_loop_A_B_left(canvas=canvas,data=data,window=root,A=lense_Info['left_lense_right'],B=lense_Info['left_lense_left'],centerx=lense_Info['left_lense_center'][0],centery=lense_Info['left_lense_center'][1])
        
        #do the right eye
        right_border=Oval_loop_A_B_left(canvas=canvas,data=data,window=root,A=lense_Info['right_lense_right'],B=lense_Info['right_lense_left'],centerx=lense_Info['right_lense_center'][0],centery=lense_Info['right_lense_center'][1])
        

        
    elif HemianopsiaType=='right':
        left_border=Oval_loop_A_B_right(canvas=canvas,data=data,window=root,A=lense_Info['left_lense_left'],B=lense_Info['left_lense_right'],centerx=lense_Info['left_lense_center'][0],centery=lense_Info['left_lense_center'][1])
        
        right_border=Oval_loop_A_B_right(canvas=canvas,data=data,window=root,A=lense_Info['right_lense_left'],B=lense_Info['right_lense_right'],centerx=lense_Info['right_lense_center'][0],centery=lense_Info['right_lense_center'][1])
        
            
    
    print (left_border)
    print(right_border)
    borders ={'Left_border': left_border,'Right_border':right_border}
    return borders

#In this function, the oval moves rightwards. 
def Oval_loop_A_B_right(data,window,A, B, centerx,centery,canvas):#A must be smaller than B
    #canvas=Canvas(window,width=width,heigh=height,bg='#fff')
    center_oval=canvas.create_oval(centerx,centery,centerx+50,centery+50, fill='#ff0000')
    
    window.update()
    #set y_pos to be the center of the canvas.
    #real =500

    data.y_pos = window.winfo_screenheight()/2
    data.x_pos = A
    
    while data.x_pos<B:
        
        oval=canvas.create_oval(data.x_pos,data.y_pos,data.x_pos+20,data.y_pos+20)
        window.update()
        time.sleep(0.1)
        data.update_xpos(data.x_pos+5)
        canvas.delete(oval)
        window.update()
    canvas.delete(center_oval)
    return data.get_and_reset()

#In this fucntion the oval moves leftwards.
def Oval_loop_A_B_left(canvas,data,window,A, B, centerx,centery):#A must be larger than B
    #create a canvas that is as big as the screen.
    #canvas=Canvas(window,width=width,heigh=height,bg='#fff')
    #create an oval in the centre. 
    center_oval=canvas.create_oval(centerx,centery,centerx+20,centery+20, fill='#ff0000')
    
   
    window.update()
    #set y_pos to be the vertical middle of the canvas.
    data.y_pos = window.winfo_screenheight()/2
    data.update_xpos (A)
    
    
    while data.x_pos>B:
        
        oval=canvas.create_oval(data.x_pos,data.y_pos,data.x_pos+20,data.y_pos+20)
        window.update()
        time.sleep(0.1)
        data.update_xpos(data.x_pos-5)
        canvas.delete(oval)
        window.update()
    canvas.delete(center_oval)
    return data.get_and_reset()




