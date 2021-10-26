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
import threading

 

width=1920
height=1080

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
        self.border_vals.append((self.x_pos,self.y_pos))
        print ('notified')
    def get_and_reset (self):
        vals=self.border_vals
        self.border_vals=[(0,0)]
        self.x_pos=0
        self.y_pos=0
        return vals
       
        

#In the width and height variables of the main loop you must enter the width and the height of the VR screen. 
def main (HemianopsiaType='left'):
    
    #create the data for xpos, y pos and the blindsdpots
    data = container()
    #create the root window
    root = Tk()
    #place the window in the right place
    Screen_height=root.winfo_screenheight()
    Screen_width=root.winfo_screenwidth()
    root.geometry((str(Screen_width)+'x'+str(Screen_height)+'+0+0'))
    #create a button for notifying and put it in the root window
    btn=ttk.Button(root, text='Notify')
    #Bind it to the notify function in the data. 
    
    btn.bind('<Button-1>',data.Notify)
    btn.grid(row=3,rowspan=1)
    root.update_idletasks()
    
    right_can='' 
    left_can=''

    #Create a thread that will run the loop of the window showing a moving dot across the window. 
    #pass it the window, so it can create a canvas and put it in there.
    #pass it the data so it can update the spos and the ypos variables as it moves the oval across the screen. 
    #also pass it the width and the hight of the scree because it will need those to make the canvas and tu run its while loop.
    
    #realcenters need to be calculated with fov_measure of particular device. 
    left_lense_center=[Screen_width/4,Screen_height/2]
    right_lense_center=[3*Screen_width/4,Screen_height/2]
    #real {'left_lense_left':250,'left_lense_right':900,'right_lense_left':1100,'right_lense_right':1800}
    lense_edges={'left_lense_left':0,'left_lense_right':Screen_width/2,'right_lense_left':Screen_width/2,'right_lense_right':Screen_width}

    Right_border = ''
    Left_border = ''
    
    canvas=Canvas(root,width=width,height=height,bg='#fff')
    canvas.grid(row=0,rowspan=3)
    
    if HemianopsiaType=='left':
        
        #do the left eye
        #Oval_loop_B_A(data=data,window=root,A=lense_edges['left_lense_right'],B=lense_edges['left_lense_left'],centerx=left_lense_center[0],centery=left_lense_center[1])

        Oval_loop_A_B_left(canvas=canvas,data=data,window=root,A=lense_edges['left_lense_right'],B=lense_edges['left_lense_left'],centerx=left_lense_center[0],centery=left_lense_center[1])
        
        #do the right eye
        Oval_loop_A_B_left(canvas=canvas,data=data,window=root,A=lense_edges['right_lense_right'],B=lense_edges['right_lense_left'],centerx=right_lense_center[0],centery=right_lense_center[1])
        

        
    elif HemianopsiaType=='right':
        Oval_loop_A_B_right(canvas=canvas,data=data,window=root,A=lense_edges['left_lense_left'],B=lense_edges['left_lense_right'],centerx=left_lense_center[0],centery=left_lense_center[1])
        
        Oval_loop_A_B_right(canvas=canvas,data=data,window=root,A=lense_edges['right_lense_left'],B=lense_edges['right_lense_right'],centerx=right_lense_center[0],centery=right_lense_center[1])
        
            
    
    print (Left_border)
    print(Right_border)
    borders ={'Left_border': Left_border,'Right_border':Right_border}
    return borders

#In this function, the oval moves rightwards. 
def Oval_loop_A_B_right(data,window,A, B, centerx,centery,canvas):#A must be smaller than B
    #canvas=Canvas(window,width=width,heigh=height,bg='#fff')
    center_oval=canvas.create_oval(centerx,centery,centerx+20,centery+20, fill='#ff0000')
    
    window.update_idletasks()
    #set y_pos to be the center of the canvas.
    #real =500

    data.y_pos = window.winfo_screenheight()/2
    data.x_pos = A
    
    while data.x_pos<B:
        
        oval=canvas.create_oval(data.x_pos,data.y_pos,data.x_pos+20,data.y_pos+20)
        window.update_idletasks()
        time.sleep(0.1)
        data.update_xpos(data.x_pos+5)
        canvas.delete(oval)
        window.update_idletasks()
    canvas.delete(center_oval)
    return data.get_and_reset()

#In this fucntion the oval moves leftwards.
def Oval_loop_A_B_left(canvas,data,window,A, B, centerx,centery):#A must be larger than B
    #create a canvas that is as big as the screen.
    #canvas=Canvas(window,width=width,heigh=height,bg='#fff')
    #create an oval in the centre. 
    center_oval=canvas.create_oval(centerx,centery,centerx+20,centery+20, fill='#ff0000')
    
   
    window.update_idletasks()
    #set y_pos to be the vertical middle of the canvas.
    data.y_pos = window.winfo_screenheight()/2
    data.update_xpos (A)
    
    
    while data.x_pos>B:
        
        oval=canvas.create_oval(data.x_pos,data.y_pos,data.x_pos+20,data.y_pos+20)
        window.update_idletasks()
        time.sleep(0.1)
        data.update_xpos(data.x_pos-5)
        canvas.delete(oval)
        window.update_idletasks()
    canvas.delete(center_oval)
    return data.get_and_reset()




if __name__ == '__main__':
    main()
