import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 on #TCP 

PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname()) #Gets the host name automatically
ADDR = (SERVER, PORT) #porting constant
BYTES = 2048 #change it later

s.connect(ADDR)

CONNECTED = True
while CONNECTED:
    msg = s.recv(BYTES) #this will be a bottle neck later as the received packet can only be 2048
    if msg is not None:
        print(msg.decode("utf-8"))
    time.sleep(5)
    print("now disconnecting...in 3 sec")
    time.sleep(5)
    s.send(bytes(f"DISCONNECT_{SERVER}", "utf-8"))
    print("SENT")
        