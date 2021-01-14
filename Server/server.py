import sys
import socket
from DFP_CONSTS import * 
from server_manager import *

if __name__ == '__main__':
    
    if (len(sys.argv) < 3 or len(sys.argv) >= 4):
        print ('Invalid input. Usage python3 server.py <server_port> <admin_passwd>')
        sys.exit()

    if (int(sys.argv[1]) < SPECIAL_PRIVELAGES_PORT):
        print ('''Invalid port number, need special privelages 
        to access the content, add a port number > 1024''')
        sys.exit()

    #Get the port and admin_passwrd
    Port = int (sys.argv[1])
    admin_passwrd = sys.argv[2]

    #creates the Server class and then begins the interaction
    s = Server(Port, admin_passwrd)
    s.begin()