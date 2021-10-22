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
    #create the container for xpos, y pos and the blindsdpots
    data = container()
    #create the root window
    root= Tk()
    #create a butting for notifying and put it in the root window
    btn=ttk.Button(root, text='Notify')
    #Bind it to the notify function in the container. 
    btn.bind('<Button-1>',data.Notify)
    btn.grid(row=3)
    #Create a thread that will run the loop of the window showing a moving dot across the window. 
    #pass it the window, so it can create a canvas and put it in there.
    #pass it the container so it can update the spos and the ypos variables as it moves the oval across the screen. 
    #also pass it the width and the hight of the scree because it will need those to make the canvas and tu run its while loop.
    left_lense_center=[500,500]
    right_lense_center=[1000,500]
    lense_edges={'lefth_lense_left':250,'left_lense_right':900,'right_lense_left':1100,'right_lense_right':1800}

    Right_border = ''
    Left_border = ''
   
    if HemianopsiaType=='left':
        #do the left eye
        Oval_thread_Le=threading.Thread(target=Oval_loop_B_A(container=data,window=root,A=lense_edges['left_lense_right'],B=lense_edges['left_lense_left'],centerx=left_lense_center(0),centery=left_lense_center(1)))
        Oval_thread_Le.start()
        Left_Border=Oval_thread_Le.join()
        #do the right eye
        Oval_thread_Ri= threading.Thread(target=Oval_loop_B_A(data,root,lense_edges['right_lense_right'],lense_edges['right_lense_left'],centerx=right_lense_center(0),centery=right_lense_center(1)))
        Oval_thread_Ri.start()
        Right_border=Oval_thread_Ri.join()
    elif HemianopsiaType=='right':
        Oval_thread_Le=threading.Thread(target=Oval_loop_A_B(data,root,lense_edges['left_lense_left'],lense_edges['left_lense_right'],centerx=left_lense_center(0),centery=left_lense_center(1)))
        Oval_thread_Le.start()
        Left_Border=Oval_thread_Le.join()
        Oval_thread_Ri=threading.Thread(target=Oval_loop_A_B(data,root,lense_edges['right_lense_left'],lense_edges['right_lense_right'],centerx=left_lense_center(0),centery=left_lense_center(1)))
        Oval_thread_Ri.start()
        Right_border=Oval_thread_Ri.join()    
    
    print (Left_border)
    print(Right_border)
    borders ={'Left_border': Left_border,'Right_border':Right_border}
    return borders


def Oval_loop_A_B(container,window,A, B, centerx,centery):
    canvas=Canvas(window,width=width,heigh=height,bg='#fff')
    canvas.create_oval(centerx,centery,centerx+20,centery+20,_Color='red')
    canvas.grid(row=0,rowspan=3)
    window.update()
    container.y_pos = 500
    container.x_pos = A
    while container.x_pos<B:
        canvas.create_oval(container.x_pos,container.y_pos,container.x_pos+20,container.y_pod+20)
        window.update()
        container.update_xpos(container.x_pos+10)
    return container.get_and_reset()
    
def Oval_loop_B_A(container,window,A, B, centerx,centery,ri_or_le):
    canvas=Canvas(window,width=width,heigh=height,bg='#fff')
    canvas.create_oval(centerx,centery,centerx+20,centery+20,_Color='red')
    canvas.grid(row=0,rowspan=3)
    window.update()
    container.y_pos = 500
    container.x_pos = B
    while container.x_pos>A:
        canvas.create_oval(container.x_pos,container.y_pos,container.x_pos+20,container.y_pod+20)
        window.update()
        container.update_xpos(container.x_pos-10)
    return container.get_and_reset()




if __name__ == '__main__':
    main('HTC_vive')
