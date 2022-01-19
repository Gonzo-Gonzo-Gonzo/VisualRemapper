import pickle
import  socket
import Camera_reader


Camera=Camera_reader. cameraStream()
r=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
        r.bind(('192.168.1.103',2000))#arbitrary port
        r.listen()
        global conn
        conn,addr=r.accept()

        #host and port on PC
        HOST='XXX.XXX.X.XXX'
        PORT= XXX

        s.connect((HOST,PORT))
        print (addr)
        Camera.start()
        print(Camera.read())
        while(True):
                receive_request()
                get_and_send()
def get_and_send():
        print('inside while loop')
        frame=Camera.read()
        frame=pickle.dumps(frame)
        print (len(frame))
        s.sendall(frame)
        print ('done')
        return
def receive_request():

        message=b''
        size =16
        while (True):
                while len( message)<size:
                        message+=conn.recv(1)
                message=pickle.loads(message)
                if message=='1':
                        return
if __name__=='__main__':
        main()

