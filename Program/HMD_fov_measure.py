from tkinter import Tk, Canvas, Frame, BOTH,ttk
import time
import tkinter 
import winsound
class Single_Canvas(tkinter.Canvas):
    def __init__(self, root,height, width,button):
        super.__init__
        self.xpos=0
        self.ypos=0
        self.invisible_areas=[(0,0)]
        self.width=width
        self.height=height
        self.button=button
        self.button.bind('<Return>',self.notifiy)
    def start_Horizontal(self):
        while self.xpos<self.width:
            oval=self.create_oval(self.xpos,self.ypos,self.xpos+1,self.ypos+1)
            winsound.Beep(2500,100)
            time.sleep(0.5)
            self.delete(oval)
            self.xpos+=1
        self.xpos=0
    def notifiy(self):
        self.invisible_areas.append(self.xpos,self.ypos)
 
class NSingle_Canvas():
    def __init__(self,place,nameOfHMD, width, height):
        #x and y are pointers that method use as they want ant then reset to 0
        self.xpos=0 
        self.ypos=0
        self.invisible_areas=[(0,0)]
        super().__init__()
        self.nameOfHMD= nameOfHMD
        self.width=width
        self.height=height
        self.canvas=Canvas(place,self,width=self.width,height=self.height,bd=0,bg='#fff')
        self.root= Tk()
        btn=ttk.Button(self.root, text='Notify')
        btn.bind('<Return>',self.Notified)
    def start_Horizontal(self):
        
        while self.xpos<self.width:
            oval=self.canvas.create_oval(self.xpos,self.ypos,self.xpos+1,self.ypos+1)
            winsound.Beep(2500,100)
            time.sleep(0.5)
            self.canvas.delete(oval)
            self.xpos+=1
        self.xpos=0
    def Notified(self):
        self.invisible_areas.append(self.xpos,self.ypos)


def main (nameofHMD='HTC_Vive',width=10000,height=10000):
    def Notify(self):
        invisible_areas.append(x_pos,y_pos)    
    root= Tk()
    btn=ttk.Button(root, text='Notify')
    btn.bind('<Return>',Notify)
    #dot_canvas=Single_Canvas(root,button=btn,width=width,height=height)    
    x_pos=0
    y_pos=0
    invisible_areas=[(0,0)]
    dot_canvas = Canvas(btn,width=width,heigh=height,bg='#fff')
    while x_pos<width:
        oval=dot_canvas.create_oval(x_pos,y_pos,x_pos+1,y_pos+1)
        winsound.Beep(2500,100)
        time.sleep(0.5)
        dot_canvas.delete(oval)
        x_pos+=1
    x_pos=0
    dot_canvas.place()
    root.mainloop() 
    
if __name__ == '__main__':
    main('HTC_vive')
