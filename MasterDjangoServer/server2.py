import socket
import threading

#remake of server.py

HEADER = 64 #bytes used in conn.recv in client handler , this header tells the server of how much length or how much bytes the msg will come from the client next...its preceeds the main msg
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname()) #Gets the host name automatically
ADDR = (SERVER, PORT) #porting constant
FORMAT = 'utf-8' #will be used to decode the socket data recieved or to send
DISCONNECT = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clientlist = []
 
def collectivesend(msg):
    for client in clientlist:
        convertedclient = client.split(",", 1)# the format is like '192.168.0.105', 62385, so it splits it and in next step it is assigned to conn and addr
        print(f"[CONVERTED CLIENT!]{convertedclient}")
        a, b = convertedclient #declared the conn and addr for each loop
        conn = a
        addr = b.replace("'", "")
        print(f"[CONVERTED CLIENT!]{conn}+++{addr}")
        # sendhandler(conn, addr, msg)
        
        sendthread = threading.Thread(target=sendhandler, args=(conn, msg))
        sendthread.start() #starts a new thread when new object fetched



def sendhandler(conn,  msg):
    print("from sendhandler")
    message = str(msg).encode(FORMAT) 
    print(f"[ENCODED DATA in utf8] {message}")
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length) #current error, addr not used
    conn.send(message)
    conn.close()


def handle_client(conn, addr): #will run concurrently for each client #STEP_2
    print(f"[NEW CONNECTION] {addr} connected.") #new connected address printed
    
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT) #gets data from client #can be a bug as the header is too small for now = 64 bytes
            if msg_length: #not null
                msg_length = int(msg_length) #converts it into a integer #tells how long the msg is comming $$$$$When connecting this will give an error of int(with base 10) but after immediately connecting it sends a connected msg so it fails as its a string 
                msg = conn.recv(msg_length).decode(FORMAT) #now it decodes the main msg (as it got the length of the main msg)

                if msg == DISCONNECT:
                    # break or
                    connected = False

                print(f"[{addr}] {msg}") #DEBUG = Prints the msg recieved from the addr specified
                if "_" in msg:
                    checkcommand = msg.split("_", 1)  #splits the msg recieved to check for commands
                    command, mainmsg =  checkcommand #assigns the array object of msgrcv splitted to two var
                    print(command) #DEBUG
                    if command == "TEST":
                        print("TESTING LOOP RUNNING!!!!!!") ##only for testing...this should be on client side
                        print(f"[COMMAND MSG RECEIVED] {mainmsg}")

                
                conn.send("SUCCESS_the server has received the msg received".encode(FORMAT)) #SEND A MSG to CLIENT confirming it got the msg
        except ValueError:
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1 - 1}")
            conn.close() #disconnects on error exception


    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1 - 1}")
    conn.close() #when the while loop is broken this is triggered
    




def start(): #setsup the server (initialises) then passes the value to handle client #STEP_1
    server.listen() #listening for new connection 
    print(f"[LISTENING] Server is Listening on {SERVER} on port {PORT}...")
    while True:
        conn, addr = server.accept() #gets the data and stores as a object helps to communicate back
        #when the object is collected now a new thread will be assigned to it with funtion handle_client()
        clientlist.append(f"{addr}") # adds the client to clientlist
        print(f"[CLIENT LIST] {clientlist}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() #starts a new thread when new object fetched

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") #how many threads for the python is running 

        ###########################################

def senddatahandler():
    print("Input Messages:")
    custommessage = input()
    collectivesend(custommessage)



        ###########################################

print("[STARTING SERVER]Server Starting....")

#starts data handler
datathread = threading.Thread(target=senddatahandler)
datathread.start() 

#starts the main function
start()

######################## method2 data input stream

        