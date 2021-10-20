from tkinter import Tk, Canvas, Frame, BOTH,ttk
import time
import tkinter 
import winsound

def main (nameofHMD='HTC_Vive',width=10000,height=10000):
    def Notify():
        invisible_areas.append(x_pos,y_pos)    
    root= Tk()
    btn=ttk.Button(root, text='Notify')
    btn.bind('<Return>',Notify)
    #dot_canvas=Single_Canvas(root,button=btn,width=width,height=height)    
    x_pos=0
    y_pos=0
    invisible_areas=[(0,0)]
    dot_canvas = Canvas(root,width=width,heigh=height,bg='#fff')
    dot_canvas.place()
    while x_pos<width:
        oval=dot_canvas.create_oval(x_pos,y_pos,x_pos+1,y_pos+1)
        root.update()
        winsound.Beep(2500,100)
        time.sleep(0.5)
        dot_canvas.delete(oval)
        x_pos+=1
    x_pos=0
    
if __name__ == '__main__':
    main('HTC_vive')
