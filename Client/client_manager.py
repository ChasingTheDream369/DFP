from socket import *
from DFP_CONSTS import *
from client_process_commands import *
import sys
from time import sleep
import threading

class Client:
    
    def __init__(self, Server_IP, Server_Port):
        self.Server_Port = Server_Port
        self.Server_IP = Server_IP
        self.username = None
        self.password = None
        self.is_SHT = None

    def get_username(self):
        '''Get the username enterd by the client'''
        return self.username
    
    def get_password(self):
        '''Gets the password of the current user/client'''
        return self.password
    
    def input_username(self):
        '''Asks the user to enter a username'''
        username = input ('Username: ')
        return username
    
    def input_password(self):
        '''Asks the user to enter a password'''
        password = input('Password: ')
        return password
    
    def input_new_password(self):
        '''Asks the user to enter a new password'''
        password = input('Enter a new Password: ')
        return password
    
    def get_commnad_exec_funcs(self, command):
        '''Gets the function realted to the command'''
        command_exec_funcs = {'CRT' : process_res_CRT, 'MSG' : process_res_MSG, 
        'DLT' :  process_res_DLT, 'EDT' : process_res_EDT, 'LST' : process_res_LST,
        'RDT' : process_res_RDT, 'UPD' : process_res_UPD, 'DWN' : process_res_DWN, 
        'RMV' : process_res_RMV, 'XIT' : process_res_XIT, 'SHT' : process_res_SHT}
        return command_exec_funcs[command]

    def forum_interation(self, conn):
        '''Begins the forum interaction and starts giving the commands and user keeps 
        inputting the commands until it has received the COMMAND_FOUND and then processes
        the command by calling the specefic command func'''
        command = None
        
        while True:
            
            if command == 'XIT' or self.is_SHT == INITIATING_SHUTDOWN:
                os._exit(os.EX_OK)
            
            command = input ('Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT: ')
            conn.send(bytes(command, FORMAT))
            
            while conn.recv(MAXIMUM_LENGTH).decode(FORMAT) != COMMAND_FOUND:
                print ('Invalid command, Try again..!')
                command = input ('Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT: ')
                conn.send(bytes(command, FORMAT))
            
            conn.send(bytes(PROCESS_COMMAND, FORMAT))
            command_func = self.get_commnad_exec_funcs(command.split()[0])
            
            if command.split()[0] == 'SHT':
                self.is_SHT = command_func(conn, command)
            else:
                command_func(conn, command)
    
    def trigger_forum_start(self, conn):
        '''Wrapper for the stating the real forum interaction after it recieves the 
        FORUM START command'''

        print ('Login successful...Enjoy the forum experience now')
        conn.send(bytes(AUTHORIZATION_COMPLETE, FORMAT))
        if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == FORUM_START:
            self.forum_interation(conn)

    def manage_new_client(self, conn):
        '''Manage the new client by sending the new password and 
        then start the forum if the user is not already logged in'''

        new_passwrd = self.input_new_password()
        conn.send(bytes(new_passwrd, FORMAT))
        recieved_state = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
        if recieved_state == USERNAME_ALREADY_LOGGEDIN:
            print ('User already in a logged in session')
        else:
            self.trigger_forum_start(conn)
    
    def manange_registered_client(self, conn, recieved_state):
        '''Keeps sending the username nad password until the 
        user is not authorised and if it is authorised then triggeer the
        stat of trigger_forum_start()'''

        while recieved_state != USER_AUTHORISED:
                            
            print ('Invalid password')
            
            if recieved_state == USERNAME_REQUIRED:
                username = self.input_username()
                conn.send(bytes(username, FORMAT))
            recieved_state = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
            
            if recieved_state == PASSWORD_REQUIRED:
                password =  self.input_password()     
                conn.send(bytes(password, FORMAT))
            
            elif recieved_state == NEW_PASSWORD:
                password =  self.input_new_password()     
                conn.send(bytes(password, FORMAT))
                if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == NEW_USER_ADDED:
                    break
            
            recieved_state = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
                    
        self.trigger_forum_start(conn)


    def Manage_authorization(self, conn):
        '''Manage the authorisation of the user it starts by getting from the server
        USERNAME_REQUIRED and then asks the user to give a name and then sends the username and if the server
        gives back that the use is already logged in the authorisation begins again and then if 
        the user gets NEW_PASSWORD then we call the mnage_new_client function otherwise if after sending the
        password we dont get that the user is loggedin we start the registered_client function'''

        if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == USERNAME_REQUIRED:
                
            username = self.input_username()
            conn.send(bytes(username, FORMAT))

            check_username = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
            
            if check_username == USERNAME_ALREADY_LOGGEDIN:
                print ("User already in the logged in session try again later..!!")
            
            else:
                
                if check_username == NEW_PASSWORD:
                    self.manage_new_client(conn)
                        
                else:
                    
                    password = self.input_password()
                    conn.send(bytes(password, FORMAT))
                    recieved_state = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
                    
                    if recieved_state != USERNAME_ALREADY_LOGGEDIN:
                        self.manange_registered_client(conn, recieved_state)
                        
                    else:
                        print ('User already in a logged in session')

    def send_handler(self, Server_alive):
        '''The thread which indefintely sends and waits for the reponse from the server
        as a background thread and if it does not gets any response then the it exits and it 
        sends these messages after every UPDATE_INTERVAL time'''

        while True:
            Server_alive.send(bytes(RESPONSE_REQUIRED, FORMAT))
            is_alive = Server_alive.recv(MAXIMUM_LENGTH).decode(FORMAT)
            if not is_alive:
                print ('\nServer is shutting down...We hope you had a unforgettable experience on the forum')
                os._exit(os.EX_OK)
            sleep(UPDATE_INTERVAL)

    def start_handling(self, conn):
        '''Begins the handling of users by starting their authorisation first
        as the sockets are alreadhy connected to the server'''

        connected = True
        while connected:
            self.Manage_authorization(conn)

    def begin(self):
        '''The first method which starts the interaction between client and server,
        first create a Server_laive which starts a thread for send_handler as a background thread
        for SHT and then call the start_handling function by the main thread which in turn waits for the connections
        on <SERVER IP> <SERVER PORT> and the send_handler happens on the same IP but <SERVER PORT +1>'''

        Server_alive = socket(AF_INET, SOCK_STREAM) 
        Server_alive.connect((self.Server_IP, self.Server_Port+1))
        send_thread = threading.Thread(name="SendHandler",target=self.send_handler, args=(Server_alive,))
        send_thread.daemon=True
        send_thread.start()
        
        conn = socket(AF_INET, SOCK_STREAM)
        conn.connect((self.Server_IP, self.Server_Port))
        self.start_handling(conn)
        
            
        


