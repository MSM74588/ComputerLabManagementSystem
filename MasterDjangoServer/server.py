import socket
import threading
# from rich.prompt import Prompt

##THis server is configured to only run at local IP 


HEADER = 64 #bytes used in conn.recv in client handler , this header tells the server of how much length or how much bytes the msg will come from the client next...its preceeds the main msg
PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname()) #Gets the host name automatically
ADDR = (SERVER, PORT) #porting constant
FORMAT = 'utf-8' #will be used to decode the socket data recieved or to send
DISCONNECT = "!DISCONNECT" #this string will be used as a sent msg to client to disconnect from the websocket , this will close the connection and disconnect

"""
CUSTOM HEADER PROTOCOLS = 3 charecter format @@@_Message Message
Therefore Parse the first 3 letter for the Command Protocol
https://www.kite.com/python/answers/how-to-parse-a-string-in-python#:~:text=Use%20str.,into%20a%20list%20of%20strings.&text=,%20'ef'%5D-,Call%20str.,number%20of%20splits%20to%20perform.
SCR = shareSCReen
LNK - openLiNK
PSH = PowerSHell
DEL = DELeteStudentFiles
SHT = ShutDown Computers
MSG = message protocol
"""





server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #using AF_INET internet protocol 
server.bind(ADDR) #data binding

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
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() #starts a new thread when new object fetched

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}") #how many threads for the python is running 



print("[STARTING SERVER]Server Starting....")

############################## * EXECUTION * #######################################
start()
# con = Prompt.ask("Disconnect from server?", choices=["disconnect", "noting"])
# if con == "/disconnect":
#     quit()
# else:
#     pass
####ADD this as another process (subprocess)

##So the current BUG is
"""
I currently need a program that can send the data from the server
and the client automatically processes it
like in server.py i have a client handler, i have to setup a server handler in the client py so it can
process the data automatically instead of sending and then receiving the data and processing
For now i am having to provoke the function (send function)
so implement a server handler so it is automatically provoked 
"""
