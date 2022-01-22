#The class in this script is instantiated by Sender.py and uses the "read" method to get the next frame.
#It collects frames from the rapsberry pi camera and puts them in a queue on a thread. 
import cv2
import pickle
import time
import struct
from queue import Queue
from threading import Thread


class cameraStream ():
        def __init__(self):
                self.stream= cv2.VideoCapture(0)
                self.stopped=False

                self.Q=Queue()
                self.thread= Thread(target=self.update,args=())
        def start(self):
                self.thread.start()
                return self
        def update(self):
                while True:
                    if self.stopped:
                                break
                        if not self.Q.full():
                                (grabbed, frame)= self.stream.read()
                                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                                if not grabbed:
                                        continue
                                else:
                                        self.Q.put(frame)
                        else:
                            time.sleep(0.1)
                self.stream.release()
        def read(self):
                return self.Q.get()
        def running (self):
                return self.more() or not self.stopped
        def more(self):
                tries=0
                while self.Q.qsize()==0 and not self.stopped and tries<5:
                        time.sleep(0.1)
                        tries +=1
                return self.Q.size>0
        def stop(self):

                self.stopped=True
                self.thread.join()




