from socket import *
from DFP_CONSTS import *
import json
import os

def process_res_CRT(conn, command):
    '''Gets the CRT reponse and then prints back the same to the user'''

    CRT_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if CRT_response == INVALID_CRT:
        print (INVALID_CRT)
    
    else:
        command_args = get_command_args(command)
        new_thread = command_args[1]

        if CRT_response == THREAD_CREATED:
            print (f'New thread {new_thread} created.')
        else:
            print (f'Thread {new_thread} already exists')

def process_res_MSG(conn, command):
    '''Gets the MSG reponse and then prints back the same to the user'''
   
    MSG_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if MSG_response == INVALID_MSG:
        print (INVALID_MSG)
    
    else:
        command_args = get_command_args(command)
        Thread_Title = command_args[1]
        if MSG_response == MESSAGE_ADDED:
            print (f'message posted in {Thread_Title}.')
        
        else:
            print (f'Thread {Thread_Title} does not exists')

def process_res_DLT(conn, command):
    '''Gets the DLT reponse and then prints back the same to the user'''

    DLT_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    if DLT_response == INVALID_DLT:
        print (INVALID_DLT)
    
    else:
        command_args = get_command_args(command)
        Thread_Title = command_args[1]
        msg_num = command_args[2]
        
        if DLT_response == MESSAGE_DELETED:
            print (f'message number {msg_num} deleted from {Thread_Title}.')
        
        elif DLT_response == INVALID_MESSAGE_NUMBER:
            print (f'Message {msg_num} is undeletable, since the message number does not exist.')
        
        elif DLT_response == NO_THREAD:
            print (f'There is no thread corresponding to {Thread_Title}')
        
        elif DLT_response == INVALID_AUTHOR:
            print (f'The user cannot delete the message since he is not the author of it')

def process_res_EDT(conn, command):
    '''Gets the EDT reponse and then prints back the same to the user'''

    EDT_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    if EDT_response == INVALID_EDT:
        print (INVALID_EDT)
    
    else:
        command_args = get_command_args(command)
        Thread_Title = command_args[1]
        msg_num = command_args[2]
        message = " ".join(command_args[3:])
        
        if EDT_response == MESSAGE_EDITED:
            print (f'message number {msg_num} edited from {Thread_Title} with the message {message}')
        
        elif EDT_response == INVALID_MESSAGE_NUMBER:
            print (f'Message {msg_num} is uneditable, since the message number does not exist.')
        
        elif EDT_response == NO_THREAD:
            print (f'There is no thread corresponding to {Thread_Title}')
        
        elif EDT_response == INVALID_AUTHOR:
            print (f'The user cannot edit the message since he is not the author of it')

def process_res_LST(conn, command):
    '''Gets the LST reponse and then prints back the smae to user
    if there is no error then it loads the reponse and prints that 
    back to the user'''
    LST_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if LST_response == INVALID_LST:
        print (INVALID_LST)
    
    else:
        
        if LST_response == NO_ACTIVE_THREADS:
            print (f'There are no active threads at the moment.')
        
        else:
            Active_threads = json.loads(LST_response)
            print (f'The list of active threads are:')
            for threads in Active_threads['Threads']:
                print (threads)


def process_res_RDT(conn, command):
    '''Gets the RDT reponse and then prints back the smae to user
    if there is no error then it loads the reposne and prints that 
    back to the user'''

    RDT_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if RDT_response == INVALID_RDT:
        print (INVALID_RDT)
    
    else:
        command_args = get_command_args(command)
        Thread_Title = command_args[1]
        if RDT_response == NO_THREAD:
            print (f'There is no thread matching the Thread title {Thread_Title}.')
        
        else:
            Thread_msgs = json.loads(RDT_response)
            
            if len(Thread_msgs['messages']) == 0:
                print (f'There are no messages in the thread {Thread_Title}')
            
            else:
                print (f'The messages in thread {Thread_Title} are:')
                for msgs in Thread_msgs['messages']:
                    print (msgs)

def process_res_UPD(conn, command):
    '''Gets the upload response from the server and print the same to user
    otherwise sends the uploads the file by interaction using the CONSTS from DFP_CONSTS, and 
    then sends back UPLOAD_SUCCESSFUL'''

    UPD_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if UPD_response == INVALID_UPD:
        print (INVALID_UPD)
    
    else:
        
        command_args = get_command_args(command)
        Thread_Title = command_args[1]
        filename = command_args[2]
        cwd = os.getcwd()
        
        if UPD_response == NO_THREAD:
                print (f'There is no thread matching the Thread title {Thread_Title}.')
        
        else:
            
            if os.path.isfile(cwd+'/'+filename):
                
                print (f"Starting the upload of the file {filename}")
                
                
                filesize = os.path.getsize(filename)
                conn.send(bytes(str(filesize), FORMAT))
                
                check_already_UPD = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
                if check_already_UPD == FILE_ALREADY_UPLOADED:
                    print (f"File {filename} had already been uploaded to the thread {Thread_Title}")

                elif check_already_UPD == WAITING_FILE_CONTENT:
                        
                    with open(filename, 'rb') as f:
                        bytesToSend = f.read(MAXIMUM_LENGTH)
                        bytes_read = len(bytesToSend)
                        conn.send(bytesToSend)
                        
                        while bytes_read < filesize:
                            bytesToSend = f.read(MAXIMUM_LENGTH)
                            bytes_read += len(bytesToSend)
                            conn.send(bytesToSend)
                
                    if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == UPLOAD_SUCCESSFUL:
                        print (f" file {filename} sucessfully uploaded..!!")
    
            else:

                print ('File does not exist in the current directory')
                conn.send(bytes(FILE_NON_EXISTENT, FORMAT))

def process_res_DWN(conn, command):
    '''Gets the download response from the server and print the same to user
    otherwise sends the START_DOWNLOAD to server and then just recieves the data from
    the server until the end of fileszie and then sends DOWNLOAD_SUCCESSFUL'''

    DWN_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if DWN_response == INVALID_DWN:
        print (INVALID_DWN)
    
    else:
        
        command_args = get_command_args(command)
        Thread_Title = command_args[1]
        filename = command_args[2]
        
        if DWN_response == NO_THREAD:
            print (f'There is no thread matching the Thread title {Thread_Title}.')
        
        elif DWN_response == THREAD_EXISTS_FILE_NOT:
            print (THREAD_EXISTS_FILE_NOT)
        
        else:
            print (f"Starting the download of the file {filename}")
            conn.send(bytes(START_DOWNLOAD, FORMAT))
            filesize = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
            conn.send(bytes(WAITING_DOWNLOAD, FORMAT))
            
            with open(filename, 'wb') as DWN_file:
                data = conn.recv(MAXIMUM_LENGTH)
                totalRecv = len(data)
                DWN_file.write(data)
                
                while totalRecv < int(filesize):
                    data = conn.recv(MAXIMUM_LENGTH)
                    totalRecv += len(data)
                    DWN_file.write(data)
                
            print ("Dowload Complete!")
            DWN_file.close()

            conn.send(bytes(DOWNLOAD_SUCCESSFUL, FORMAT))
            print (f" file {filename} sucessfully downloaded..!!")

            
def process_res_RMV(conn, command):
    '''Gets the remove response from the server and print the same to user
    otherwise sends the START_REMOVING to server and prints THREAD_REMOVED to
    show that thread has been removed'''

    RMV_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if RMV_response == INVALID_RMV:
        print (INVALID_RMV)
    
    else:
        
        command_args = get_command_args(command)
        Thread_Title = command_args[1]

        if RMV_response == NO_THREAD:
            print (f'There is no thread matching the Thread title {Thread_Title}.')
        
        elif RMV_response == THREAD_EXISTS_AUTHOR_WRONG:
            print (THREAD_EXISTS_AUTHOR_WRONG)
        
        else:
            print (f"Removing the thread {Thread_Title}")
            conn.send(bytes(START_REMOVING, FORMAT))

            if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == THREAD_REMOVED:
                print (f'Thread {Thread_Title} successfully removed.')


def process_res_XIT(conn, command):
    '''Gets the XIT response and prints that to the user but 
    the real exit happens in the cforum interactoin in the client_manger
    wher is XIT is initiated teh user just exits the program'''

    XIT_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if XIT_response == INVALID_XIT:
        print (INVALID_XIT)
    
    else:
        print ("Goodbye...I am leaving the forum it was an amazing experience")

def process_res_SHT(conn, command):
    '''Process the SHT response to be printed on the client side and then 
    the real shut down happens through the background i am alive thread which keeps
    sending the server messages and if it does not recieve the nit exits'''

    SHT_response = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)
    
    if SHT_response == INVALID_SHT:
        print (INVALID_SHT)
    
    else:

        if SHT_response == INVALID_ADMIN_PASSWORD:
            print ('Admin password entered was wrong, the server can''t be closed')
        
        elif SHT_response == INITIATING_SHUTDOWN:
            print ('Server is shutting down...We hope you had a unforgettable experience on the forum')
    
    return SHT_response

def get_command_args (command):
    '''get the list of all the command line args given'''
    command_args = command.split()
    return command_args