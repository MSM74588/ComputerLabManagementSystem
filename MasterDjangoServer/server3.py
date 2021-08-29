import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 on #TCP 

PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname()) #Gets the host name automatically
ADDR = (SERVER, PORT) #porting constant
QUEUE = 5 #will serve this number of computer simultaneously
BYTES = 2048 #change it later

handle_client_allow = False


ACCEPT_REQ = True

try:
    s.bind(ADDR)
except:
    print("[ERROR] Cannot Bind to port")

s.listen(QUEUE)

clientlist = []

def addclient():
    while ACCEPT_REQ:
        clientsocket, addr = s.accept() #will accept request
        print(f"[NEW CONNECTION] {addr} connected!")
        clientsocket.send(bytes(f"[HELLO FROM {SERVER}]", "utf-8"))
        clientlist.append(clientsocket) # adds the client to clientlist
        print(clientlist)
        if client_handler.called:
            pass
        if not client_handler.called:
            client_handler()
            client_handler.called = True


def sendmsg():
    #add a msg paramater later
    while True:
        if clientlist is not None:
            print("input msg")
            msg = input()
            if msg is not None:
                for client in clientlist:
                    client.send(bytes(f"{msg}", "utf-8")) #clientsocket
                    #TASK add Disconnect
                

def close(targetaddr):
    print(f"[CLOSING] {targetaddr}") #DEBUG
    targetaddr.close()

def client_handler():
    client_handler.called = False       #BUG function is valid but not called properly is not RECIEVING DATA
    while client_handler.called:
        receivedmsg = s.recv(BYTES).decode("utf-8")
        print(receivedmsg)
        if receivedmsg:
            if "_" in receivedmsg:
                checkcommand = receivedmsg.split("_", 1)
                command, mainmsg =  checkcommand #assigns the array object of msgrcv splitted to two var
                print(checkcommand) #DEBUG
                if command == "SUCCESS":
                    print("SUCCESS") ##only for testing...this should be on client side
                    print(f"[COMMAND MSG RECEIVED] {receivedmsg} MSG= {mainmsg}")
                if command == "DISCONNECT":
                    print("DISCONNECT") ##only for testing...this should be on client side
                    # mainmsg.close()#DEBUG #replace this with close command
                    targetaddr = mainmsg
                    close(targetaddr)




#########################

print(f"[SERVER STARTED] listening on {SERVER} on {PORT}")

addclientthread = threading.Thread(target=addclient).start() 
datathread = threading.Thread(target=sendmsg).start() 
cientthread = threading.Thread(target=client_handler).start() 


   
    
    # clientsocket.send(bytes("welcome to the server", "utf-8"))
        

