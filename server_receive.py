from os import set_inheritable
import socket, pickle


HOST = "192.168.1.204" #IP of the computer that will receive the data from the Pi
PORT = 50007 #An arbitrary port


buffer = 4096 #The max number of bytes to be recevied per packet. Default 4096 but this is v small. Max seems to be 10000000000 before memory errors pop up.


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Instantiate socket object
s.bind((HOST, PORT)) #Affix IP and Port to socket
s.listen(1) #Begin listening for connections/transmissions
conn, addr = s.accept() #Accept any connection
print('Connected by', addr) #Print the IP that has made a connection (should be the pi, e.g. 192.168.1.113)

while 1: 
    data = conn.recv(buffer) #Receive bytes from the connection, maximum number of bytes set by buffer that we declared before
    if not data: break #If no data received, break out of loop
    data_arr = pickle.loads(data) #Convert 
    print("Received",repr(data_arr)) #Print a representation of the received data.
    conn.send(data) #Send the data back, or anything, to acknowledge receipt of data.
conn.close() # Close connection.