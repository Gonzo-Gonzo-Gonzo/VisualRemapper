from tkinter import Tk, Canvas, Frame, BOTH,ttk
import time
import tkinter 
import winsound
import threading

class container():
    x_pos=0
    y_pos=0
    invisible_areas=[(0,0)]

    def update_xpos(self,int):
        self.x_pos=int
    def update_ypos(self,int):
        self.y_pos=int
    def Notify(self,thing):
        print (thing)
        self.invisible_areas.append((self.x_pos,self.y_pos))
        print ('notified')
    def close (self):
        print (self.invisible_areas)

def main (self,nameofHMD='HTC_Vive',width=1000,height=1000):
    #create the container for xpos, y pos and the blindsdpots
    data = container()
    #create the root window
    root= Tk()
    #create a butting for notifying and put it in the root window
    btn=ttk.Button(root, text='Notify')
    #Bind it to the notify function in the container. 
    btn.bind('<Button-1>',data.Notify)
    btn.pack()
    #Create a thread that will run the loop of the window showing a moving dot across the window. 
    #pass it the window, so it can create a canvas and put it in there.
    #pass it the container so it can update the spos and the ypos variables as it moves the oval across the screen. 
    #also pass it the width and the hight of the scree because it will need those to make the canvas and tu run its while loop.
    Oval_thread=threading.Thread(target=Oval_loop(data,root,height,width))
    
    
    #line =dot_canvas.create_line(10,10,100,100,activefill="#000000" )
    data.update_ypos(500)
    data.update_xpos(0) 
    
    data.x_pos=0
    data.close()

def Oval_loop(container,window,height,width):
    #create the canvas and put it in the window 
    canvas= Canvas(window,width=width,heigh=height,bg='#fff')
    canvas.pack()
    #update the window to make sure the canvas is included!
    window.update()
    #use x_pos as a pointer to the place in the screen that the canvas has been in.
    while container.x_pos<width:
        #draw an oval in x_pos (it stars at 0 then 10 in the secon itteration, 20,30,40,etc)
        oval=canvas.create_oval(container.x_pos,container.y_pos,container.x_pos+5,container.y_pos+5)
        #update the window to show the oval. this also registers a click in the n otify buttn?
        window.update_idletasks()
        window.update()
        #winsound.Beep(2500,100)#ADD A BEEP TO MAKE THE ui MORE FIRENDLY, COORDINATE IT WITHT EH MOVEMENT OF THE OVAL
        #give the user a moment to se the oval.
        time.sleep(0.5)
        #update to register events of button
        window.update()
        canvas.delete(oval)
        #update to shwo deletion. 
        window.update_idletasks()
        window.update()
        #increase x_pos
        container.update_xpos(container.x_pos+10)





if __name__ == '__main__':
    main('HTC_vive')
