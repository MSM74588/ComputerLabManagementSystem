import socket
from rich.prompt import Prompt
from rich.console import Console

console = Console()
HEADER = 64 #bytes used in conn.recv in client handler , this header tells the server of how much length or how much bytes the msg will come from the client next...its preceeds the main msg
PORT = 5051
FORMAT = 'utf-8' #will be used to decode the socket data recieved or to send
DISCONNECT = "!DISCONNECT" #this string will be used as a sent msg to client to disconnect from the websocket , this will close the connection and disconnect
SERVER = "192.168.0.105" #Local IP with respect to the ROUTER
ADDR = (SERVER, PORT)

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



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR) #instead of bind here we are using connect as of server


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message) #calculates the msg length for the HEADER
    send_length = str(msg_length).encode(FORMAT) #now it encodes in UTF-8 to send, converts th int into a encoded string
    send_length += b' ' * (HEADER - len(send_length)) #byte space multipled by header - len... it checks the length of msg then it substracts from 64 thus giving the blanks needed to be add as it must be 64 byte
    client.send(send_length) #sends the header string
    client.send(message) #now it sends the actual message
    rcvmsg = client.recv(2048).decode(FORMAT) #print BUG what msg is recieved from the server after sending the msg (used 2048 , means can handle only 2048 bytes, CAN BE A BUG LATER its best to implement by msg length)
    # @BUG ^^ TOTAL DUPLEX NOT POSSIBLE AS IT CAN RECEIVE ONLY UPTO 2048 Bytes
    if "_" in rcvmsg:
        checkcommand = rcvmsg.split("_", 1)  #splits the msg recieved to check for commands
        command, mainmsg =  checkcommand #assigns the array object of msgrcv splitted to two var
        if command == "SUCCESS":
            console.print("SUCCESS", style="reverse green") ##only for testing...this should be on client side
            print(f"[COMMAND MSG RECEIVED] {rcvmsg} MSG= {mainmsg}")

######################## main #############################3
STAY_CONNECTED = True
while STAY_CONNECTED:
    print("Input Messages:")
    custommessage = input()
    
    ##Disconnect msg    
    if custommessage == "/disconnect":
        name = Prompt.ask("Disconnect from server?", choices=["y", "n"])
        send(DISCONNECT)
        print("Disconected from SERVER")
        quit() #Exits the program
    else:
        send(custommessage) #send function processes the msg and sends
