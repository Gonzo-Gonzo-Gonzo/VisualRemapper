import cv2

cap=cv2.VideoCapture(0)
succesfull_attempts=0
while cap.isopen():
    for i in range (1,100):
        grab,frame=cap.read()
        if grab:
            succesfull_attempts+=1
        file=open ('c:\\Desktop\\Frames\\d%.txt'%(i),'w')
        for s in frame:
            file.write(s)

print ('extraction complete')

        

