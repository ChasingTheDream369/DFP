from socket import *
import threading
from socket import *
from DFP_CONSTS import *
import os
from server_process_commands import *
import sys
from time import sleep

t_lock = threading.Condition()

class Server:
    
    def __init__(self, Port, admin_passwrd):
        self.Port = Port
        self.admin_passwrd = admin_passwrd
        self.Address = '127.0.0.1'
        self.registered_users = []
        self.active_users = []
        self.logged_in_users = []
        self.is_authorised = None
        self.valid_commands = ['CRT', 'MSG', 'DLT', 'EDT', 'LST', 
        'RDT', 'UPD', 'DWN', 'RMV', 'XIT', 'SHT']
        self.SHT_initiated = None
        self. XIT_initiated = None
        self.waiting_users = []

    def get_port(self):
        return self.port
    
    def get_address(self):
        return self.Address
    
    def get_credentials(self):
        '''Read the credntials file and if not found then raise an error'''
        try:
            with open('credentials.txt') as cr:
                credentials = cr.read().split('\n')
                for user_details in credentials:
                    self.registered_users.append({'username' : user_details.split(' ')[0],  'password' : user_details.split(' ')[1]})
                cr.close()
        
        except FileNotFoundError as f:
            print ('File credentials.txt not found in the current directory, Course forum cannot work...Try again..!!')
            os._exit(os.EX_OK) 
    
    def get_valid_commands(self):
        '''Get all the valid commands for the user'''
        return self.valid_commands

    def get_usernames(self):
        '''get the list of all registered usernames'''
        all_users = [users['username'] for users in self.registered_users]
        return all_users

    def get_password(self, username):
        '''get the password of user'''
        for dets in self.registered_users:
            if dets['username'] == username:
                return dets['password']

    def get_commnad_exec_funcs(self, command):
        '''Get the function name from the command acronym'''

        command_exec_funcs = {'CRT' : process_CRT, 'MSG' : process_MSG, 
        'DLT' :  process_DLT, 'EDT' : process_EDT, 'LST' : process_LST, 
        'RDT' : process_RDT, 'UPD' : process_UPD, 'DWN' : process_DWN, 
        'RMV' : process_RMV, 'XIT' : process_XIT, 'SHT' : process_SHT}
        return command_exec_funcs[command]
   
    def forum_interact(self, conn, username, addr):
        '''Begins the forum interaction'''
        global t_lock
        recv_comm = None        
        
        while True:
            #if the users enter XIT then break the loop and then go to accept more connections
            if recv_comm == 'XIT':
                break
            
            #Server exits after the SHT fucntion is called
            elif self.SHT_initiated == INITIATING_SHUTDOWN:
                print ('Server shutting down..BYE BYE')
                os._exit(os.EX_OK) 

            #gets the command to begin its interaction'''    
            recv_comm = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
            print (f'{username} issued {recv_comm.split()[0]}')
            
            if recv_comm == 'XIT':
                self.active_users.remove(conn)
                self.logged_in_users.remove(username)
                self.XIT_initiated = True
                print (f'{username} just left the session..!!\n Waiting for more connections')

            #Keeps getting the commands until a vaid command is given''' 
            while recv_comm.split()[0] not in self.get_valid_commands():
                conn.send(bytes(INVALID_COMMAND, FORMAT))
                print ('Invalid command...!!')
                recv_comm = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
            
            #if it comes out of the loop that measn the comamdn if found'''
            conn.send(bytes(COMMAND_FOUND, FORMAT))
            
            #initates the command thereafter
            if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == PROCESS_COMMAND:
                
                comm_func = self.get_commnad_exec_funcs(recv_comm.split()[0])
                
                if recv_comm.split()[0] == 'SHT':
                    self.SHT_initiated = comm_func(conn, recv_comm, username, self.admin_passwrd)
                
                else:
                    comm_func(conn, recv_comm, username, t_lock)   

    def trigger_forum_start(self, conn, addr, username):
        '''if the client gives AUTHORIZATION_COMPLETE, then  user is added to logged in users
        and then forum interaction is started'''

        if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == AUTHORIZATION_COMPLETE:
            self.logged_in_users.append(username)
            print (f'{username} successfully logged in..!!')
            conn.send(bytes(FORUM_START, FORMAT))
            print ('Forum interaction beginning enjoy your experience..!!')
            self.forum_interact(conn, username, addr)

    def handle_new_client(self, conn, addr, username):
        ''' If it is a new user then firstly checks if it is not logged in
        just in case if the user did appear in the middle and then otherwise 
        adds the user to credentials file and then start the forum for the user'''

        print ('New user')
        conn.send(bytes(NEW_PASSWORD, FORMAT))
        new_pass = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
        
        if username in self.logged_in_users:
            print ('user already in active session..!!')
            conn.send(bytes(USERNAME_ALREADY_LOGGEDIN, FORMAT))
        else: 
            
            self.registered_users.append({'username' : username, 
            'password' : new_pass})
            with open('credentials.txt', 'a') as cr:
                cr.write(f'\n{username} {new_pass}')
            conn.send(bytes(NEW_USER_ADDED, FORMAT))   
            self.trigger_forum_start(conn, addr, username)
    
    def handle_already_registered_client(self, conn, addr, username):
        '''cheks if the client is not in logged in users and then asks for the 
        password and follows the smae process unitl it has found the right password
        , also allows the other user to login ifthe invalid password is added and if 
        the username if found then it triggers the beginning of forum and handles the
        commands'''

        print (f'Password for {username} required')
        conn.send(bytes(PASSWORD_REQUIRED, FORMAT))
        recieved_pass = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
        
        if username in self.logged_in_users:
            print ('user already in active session..!!')
            conn.send(bytes(USERNAME_ALREADY_LOGGEDIN, FORMAT))
        
        else:
            
            while recieved_pass != self.get_password(username):
                
                print ('Invalid password')
                conn.send(bytes(USERNAME_REQUIRED, FORMAT))
                
                username = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
                
                if username not in self.get_usernames():
                    self.handle_new_client(conn, addr, username)
                    break
                
                conn.send(bytes(PASSWORD_REQUIRED, FORMAT))
                recieved_pass = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
        
        
            conn.send(bytes(USER_AUTHORISED, FORMAT))
            self.trigger_forum_start(conn, addr, username)
            
    def authorise(self, conn, addr):
        '''For the authorising the client it manages the two way communication and 
        sends and recieve the messages acoording to the state, if the username is already in the logged
        in users then the process will start again, otherwise if it is a new user the handle_new_client
        method is called otherwise already_)registerd method is called'''

        conn.send(bytes(USERNAME_REQUIRED, FORMAT))
        username = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
        print ('User joined the connection..!!')
        
        if username in self.logged_in_users:
            print ('user already in active session..!!')
            conn.send(bytes(USERNAME_ALREADY_LOGGEDIN, FORMAT))
        
        else:
            
            if username not in self.get_usernames():
                              
                self.handle_new_client(conn, addr, username)
            
            else :
                
                self.handle_already_registered_client(conn, addr, username)
                
    
    def Manage_Client(self, conn, addr):
        ''' this is the main function which manages the real 
        response/request connection with the server and then 
        start the authorisation of each of the clients that come
        here and checks if the XIT is initiated then moves out i.e someone 
        exitted and then set the XIT to false again'''

        print(f"[NEW CLIENT] {addr} connected.")
        self.active_users.append(conn)
        connected = True
        while connected:
            self.get_credentials()
            self.authorise(conn, addr)
            if self.XIT_initiated == True:
                connected = False
                self.XIT_initiated = False
        
    def send_handler(self, clients):
        '''Indefinitely sends the ALIVE message to all the wating users-this 
        wating users will et updated as more users will be coming and then server 
        will start sending the same message to all until it exits/ shut downs'''

        while True:
            if self.waiting_users:
                for users in self.waiting_users:
                    if users.recv(MAXIMUM_LENGTH).decode(FORMAT) == RESPONSE_REQUIRED:
                        users.send(bytes(ALIVE, FORMAT))
    
    def alive_handling(self, clients):
        '''Gets the connections from each of the client that gets fet activated and then
        sends them to another thread send_handler where the server keeps sending the i am
        alive message to all the wating users/specila sockets of clients which it has accepted on this 
        socket'''

        clients.listen()
        
        while True:
            alives, addr = clients.accept()
            self.waiting_users.append(alives)
            thread = threading.Thread(target=self.send_handler, args=(clients,), daemon=True)
            thread.start()

    # used this link as a refernce to start with the server 
    # code https://www.techwithtim.net/tutorials/socket-programming/
    def server_handling(self, s):
        '''Listens for the connections and then accept the incoming connections
        after that begins the thread for the current client by calling the Manage_Client
        function'''

        s.listen()
        print ('[LISTENING]..Server ready to accept connections')
        
        while True:
            conn, addr = s.accept()
            self.active_users.append(conn)
            thread = threading.Thread(target=self.Manage_Client, args=(conn, addr), daemon=True)
            thread.start()
        
        s.close()
    
    def begin(self):
        '''The first method which starts the interaction between client and server,
        first create a clients socket which starts a thread for alive handling as a background thread
        for SHT and then call the server_handling function by the main thread which in turn waits for the connections
        on <SERVER IP> <SERVER PORT> and the alive handling happens on the same IP but <SERVER PORT +1>'''

        clients = socket(AF_INET, SOCK_STREAM)
        clients.bind((self.Address, self.Port+1))
        thread = threading.Thread(target=self.alive_handling, args=(clients,), daemon=True)
        thread.start()

        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.Address, self.Port))
        
        self.server_handling(s)

    