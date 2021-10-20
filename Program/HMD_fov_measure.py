from tkinter import Tk, Canvas, Frame, BOTH,ttk
import time
import tkinter 
import winsound

class container():
    x_pos=0
    y_pos=0
    invisible_areas=[(0,0)]

    def update_xpos(self,int):
        self.x_pos=int
    def update_ypos(self,int):
        self.y_pos=int
    def Notify(self):
        self.invisible_areas.append((self.x_pos,self.y_pos))
    def close (self):
        print (self.invisible_areas)

def main (nameofHMD='HTC_Vive',width=1000,height=1000):
    data = container()
    root= Tk()
    btn=ttk.Button(root, text='Notify')
    btn.bind(data.Notify())
    btn.pack()
    #dot_canvas=Single_Canvas(root,button=btn,width=width,height=height)    
    
    dot_canvas = Canvas(root,width=width,heigh=height,bg='#fff')
    #line =dot_canvas.create_line(10,10,100,100,activefill="#000000" )
    dot_canvas.pack()
    root.update()
    data.update_ypos(500)
    data.update_xpos(0) 
    while data.x_pos<width:
        oval=dot_canvas.create_oval(data.x_pos,data.y_pos,data.x_pos+5,data.y_pos+5)
        root.update_idletasks()
        root.update()
        #winsound.Beep(2500,100)#ADD A BEEP TO MAKE THE ui MORE FIRENDLY, COORDINATE IT WITHT EH MOVEMENT OF THE OVAL
        time.sleep(0.5)
        dot_canvas.delete(oval)
        root.update_idletasks()
        root.update()
        data.update_xpos(data.x_pos+10)
    data.x_pos=0
    data.close()
    
if __name__ == '__main__':
    main('HTC_vive')
