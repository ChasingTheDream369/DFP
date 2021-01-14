import socket
import sys
from client_manager import *

if __name__ == '__main__':
    
    if (len(sys.argv) < 3 or len(sys.argv) >= 4):
        print ('Invalid input. Usage python3 server.py <server_IP> <server_port>')
        sys.exit()
    
    #Gets the Server_IP and Server_Port
    Server_IP = sys.argv[1]
    Server_Port = int(sys.argv[2])

    #Creates the Client class and then begins the interaction
    c = Client(Server_IP, Server_Port)
    c.begin()
    


