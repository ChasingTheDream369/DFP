from socket import *
import threading
from socket import *
from DFP_CONSTS import *
import os
import json

SERVER_STATE = {
    'Threads' : [],
    'Files' : []
}
# Used the discussion here as a reference to find the that the path exists or not
# https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
def process_CRT(conn, command, username, t_lock):
    ''' Creates a new thread in the current working 
    directory with covering all the error handling cases'''

    command_args = get_command_args(command)
    if len(command_args) != 2:
        conn.send(bytes(INVALID_CRT, FORMAT))
        print (INVALID_CRT)
    
    else :
        
        Thread_Title = command_args[1]
        CRT_process_and_exception_handle (Thread_Title, username, conn, t_lock)
                                
def process_MSG(conn, command, username, t_lock):
    ''' Posts a message to the given thread 
    with covering all the error handling cases'''

    command_args = get_command_args(command)
    
    if len(command_args) < 3:
        conn.send(bytes(INVALID_MSG, FORMAT))
        print (INVALID_MSG)
    
    else :
        
        Thread_Title = command_args[1]
        message_num_last = 0
        message = " ".join(command_args[2:]) 

        MSG_process_and_exception_handle (Thread_Title, username, conn, message, message_num_last, t_lock)
        

def process_DLT(conn, command, username, t_lock):
    ''' Deletes the the given message number in the particular thread 
    with covering all the error handling cases'''

    command_args = get_command_args(command)
    if len(command_args) != 3:
        conn.send(bytes(INVALID_DLT, FORMAT))
        print (INVALID_DLT)
    
    else :
        Thread_Title = command_args[1]
        
        try:
            msg_num = int(command_args[2])
            DLT_process_and_exception_handle (msg_num, Thread_Title, username, conn, t_lock)
        
        except Exception as e:
            print (e)
            conn.send(bytes(INVALID_DLT, FORMAT))

def process_EDT(conn, command, username, t_lock):
    ''' Edits the the given message number in the particular thread 
    with the given message paralleled with covering all the error handling cases'''

    command_args = get_command_args(command)
    
    if len(command_args) < 4:
        conn.send(bytes(INVALID_EDT, FORMAT))
        print (INVALID_EDT)
    
    else:
        Thread_Title = command_args[1]
        try:
            msg_num = int(command_args[2])
            new_msg = " ".join(command_args[3:])
            EDT_process_and_exception_handle (msg_num, Thread_Title, username, conn, new_msg, t_lock)
        
        except Exception as e:
            print (e)
            conn.send(bytes(INVALID_EDT, FORMAT))
        
        
def process_LST(conn, command, username, t_lock):
    ''' Lists all the active threads at the moment
    with covering all the error handling cases'''

    command_args = get_command_args(command)
    if len(command_args) != 1:
        conn.send(bytes(INVALID_LST, FORMAT))
        print (INVALID_LST)
    
    else:
        
        if len(SERVER_STATE['Threads']) == 0:
            conn.send(bytes(NO_ACTIVE_THREADS, FORMAT))
            print ('There are no active threads at the moment..!!')
        else:
            Active_threads = list_messages(t_lock)
            list_threads = json.dumps(Active_threads)
            conn.send(bytes(list_threads, FORMAT))
            print ('Threads successfully listed..!!')

def process_RDT(conn, command, username, t_lock):
    ''' Read all the messages and fiels uploaded to a 
    particular thread with covering all the error handling cases'''

    command_args = get_command_args(command)
    if len(command_args) != 2:
        conn.send(bytes(INVALID_RDT, FORMAT))
        print (INVALID_RDT)
    
    else:
        
        Thread_Title = command_args[1]
        if check_thread_exists(Thread_Title) is False:
            conn.send(bytes(NO_THREAD, FORMAT))
            print (f'There is no thread corresponding to the title-{Thread_Title}')
        
        else:
            
            Thread_messages = read_messages(Thread_Title, t_lock)
            list_messages = json.dumps(Thread_messages)
            conn.send(bytes(list_messages, FORMAT))
            print (f'Successfully read all messages from {Thread_Title}')

# Based on the discussion done in this video - 
# https://www.youtube.com/watch?v=LJTaPaFGmM4
def process_UPD(conn, command, username, t_lock):
    ''' Uploads the given file to the given threads
    with covering all the error handling cases'''

    command_args = get_command_args(command)
    if len(command_args) != 3:
        conn.send(bytes(INVALID_UPD, FORMAT))
        print (INVALID_UPD)
        
    else:
        
        Thread_Title = command_args[1]
        filename = command_args[2]
        UPD_process_and_exception_handle (Thread_Title, username, conn, filename, t_lock)

def process_DWN(conn, command, username, t_lock):
    ''' Downloads the given file from the given thread
    with covering all the error handling cases'''

    command_args = get_command_args(command)
    
    if len(command_args) != 3:
        conn.send(bytes(INVALID_DWN, FORMAT))
        print (INVALID_DWN)
    
    else:
        
        Thread_Title = command_args[1]
        filename = command_args[2]
        
        DWN_process_and_exception_handle (Thread_Title, username, conn, filename, t_lock)

def process_RMV(conn, command, username, t_lock):
    ''' Removes the given threads from the current 
    working directory and also removes all the file 
    associated with it with covering all the error handling cases'''

    command_args = get_command_args(command)
    if len(command_args) != 2:
        conn.send(bytes(INVALID_RMV, FORMAT))
        print (INVALID_RMV)

    else :
        
        Thread_Title = command_args[1]
        RMV_process_and_exception_handle (Thread_Title, username, conn, t_lock)
        
    
def process_XIT(conn, command, username, t_lock):
    ''' Removes the current client from the list of active clients 
    and remvoes all the threads associated with it'''

    command_args = get_command_args(command)
    if len(command_args) != 1:
        conn.send(bytes(INVALID_XIT, FORMAT))
        print (INVALID_XIT)
    
    else:
        conn.send(bytes(SERVER_STATE_UPDATED_XIT, FORMAT))

def process_SHT(conn, command, username, admin_passwrd):
    ''' IF the admin password given matches the real admin_psswrd
    then close the server abruptly and close the connections with all the
    clients'''

    is_SHT_Sucess = None
    
    command_args = get_command_args(command)
    if len(command_args) != 2:
        conn.send(bytes(INVALID_SHT, FORMAT))
        print (INVALID_SHT)
        is_SHT_Sucess = INVALID_SHT
   
    else:
        
        entered_admin_passwrd = command_args[1]
        
        if entered_admin_passwrd != admin_passwrd:
            conn.send(bytes(INVALID_ADMIN_PASSWORD, FORMAT))
            print ('The admin_password given is invalid..!!')
            is_SHT_Sucess = INVALID_ADMIN_PASSWORD
        
        else:
            Initiate_SHT(conn)
            is_SHT_Sucess = INITIATING_SHUTDOWN
    
    return is_SHT_Sucess

# #################################################################### #
#                     MSG SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #
def MSG_SERVER_STATE_UPDATE(Thread_Title, username, conn, message, message_num_last):
    '''Update the SERVER_STATE dictoinary by adding the message and 
    add the message in the file by opening it in the append mode'''

    for thread in SERVER_STATE['Threads']:
        if thread['name'] == Thread_Title:
            message_num_last = last_msg_num(Thread_Title)
            thread['messages'].append({'id' : message_num_last + 1,
            'author' : username, 'message' : f'{message_num_last + 1} {username}: {message}'})

    cwd = os.getcwd()

    if os.path.exists(cwd+'/'+Thread_Title):
        with open(Thread_Title, 'a') as Thread:
            Thread.write(f'{message_num_last + 1} {username}: {message}\n')
        conn.send(bytes(MESSAGE_ADDED, FORMAT))
        print ('Message successfully added')

def MSG_process_and_exception_handle (Thread_Title, username, conn, message, message_num_last, t_lock):
    '''Excpetion hadnling for MSG and then execution of the real
    message functionality if no error raised'''

    if check_thread_exists(Thread_Title) is False:
        conn.send(bytes(THREAD_DOES_NOT_EXIST, FORMAT))
        print (f'Thread {Thread_Title} does not exist')
    
    else:
        
        with t_lock:
            
            MSG_SERVER_STATE_UPDATE(Thread_Title, username, conn, message, message_num_last)
            t_lock.notify()

# #################################################################### #
#                     CRT SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #

def CRT_SERVER_STATE_UPDATE(Thread_Title, username, conn):
    '''Updates the SERVER_STATE with respect to the CRT and creates 
    a file with the thread name in the cwd and writes of the username 
    in the first line of it, also add the dictionary of thread in the SERVER_STATE'''

    with open(Thread_Title, 'w+') as Thread:
        Thread.write(username+'\n')
            
    conn.send(bytes(THREAD_CREATED, FORMAT))
        
    print (f'Thread {Thread_Title} created')
    
    SERVER_STATE['Threads'].append({'name' : Thread_Title, 
        'creator' : username, 'messages' : []})

def CRT_process_and_exception_handle (Thread_Title, username, conn, t_lock):
    '''Excpetion hadnling for CRT and then execution of the real
    create functionality if no error raised'''

    cwd = os.getcwd()

    if check_thread_exists(Thread_Title):
        conn.send(bytes(THREAD_EXISTS, FORMAT))
        print (f'Thread {Thread_Title} already exists')
    
    else:
        
        with t_lock:
            
            CRT_SERVER_STATE_UPDATE(Thread_Title, username, conn)
            t_lock.notify()
            
# #################################################################### #
#                     DLT SPECIFIC HELPER FUNCTIONS                #
# #################################################################### #

def DLT_SERVER_STATE_UPDATE(Thread_Title, username, message_number, t_lock):
    '''Updates the SERVER_STATE with respect to the DLT and then writes the file 
    again by writing the joined(\n) version of the new_content list, then remove the
    given message from the SERVER_STATE['threads']['messages']'''

    for threads in SERVER_STATE['Threads']:
            if threads['name'] == Thread_Title:
                for message in threads['messages']:
                    if message['id'] is not None:
                        if message['id'] > message_number: 
                            new_msg_id = message['id'] - 1
                            message['id'] = new_msg_id
                            needed_msg = ' '.join(message['message'].split(' ')[1:]).strip()
                            num_message = str(new_msg_id)
                            new_msg = f'{num_message} {needed_msg}'
                            message['message'] = new_msg
    
    new_content = read_messages(Thread_Title, t_lock)
    author = find_thread_author(Thread_Title)
    new_content['messages'].insert(0, author)

    with open(Thread_Title, "w") as outfile:
        outfile.write("\n".join(new_content['messages']))
        outfile.write('\n')

def delete_message(Thread_Title, username, message_number, t_lock):
    '''Create the new_content list for writing the new content 
    to the thread after removing the message from the file and managin the 
    message numbers ahead of it'''

    with t_lock:
        
        for threads in SERVER_STATE['Threads']:
            if threads['name'] == Thread_Title:
                for message in threads['messages']:
                    if message['id'] == message_number: 
                        threads['messages'].remove(message)
        
        DLT_SERVER_STATE_UPDATE(Thread_Title, username, message_number, t_lock)
        t_lock.notify()

def DLT_process_and_exception_handle (msg_num, Thread_Title, username, conn, t_lock):
    '''Excpetion handling for DLT and then execution of the real
    create functionality if no error raised'''

    if msg_num < 1 or msg_num > find_num_msgs(Thread_Title): 
        conn.send(bytes(INVALID_MESSAGE_NUMBER, FORMAT))
        print (f'Message {msg_num} is undeletable')
        
    elif check_thread_exists(Thread_Title) is False:
        conn.send(bytes(NO_THREAD, FORMAT))
        print (f'There is no thread corresponding to {Thread_Title}')
    
    elif find_author(Thread_Title, msg_num) != username:
        conn.send(bytes(INVALID_AUTHOR, FORMAT))
        print (f'The user cannot delete the message since he is not the author of it')
    
    else :
        delete_message(Thread_Title, username, msg_num, t_lock)
        conn.send(bytes(MESSAGE_DELETED, FORMAT))
        print (f'Message {msg_num} successfully deleted from {Thread_Title}')

# #################################################################### #
#                     EDIT SPECIFIC HELPER FUNCTIONS                #
# #################################################################### #
def EDT_process_and_exception_handle (msg_num, Thread_Title, username, conn, new_msg, t_lock):
    '''Excpetion handling for EDT and then execution of the real
    create functionality if no error raised'''

    if msg_num < 1 or msg_num > find_num_msgs(Thread_Title): 
        conn.send(bytes(INVALID_MESSAGE_NUMBER, FORMAT))
        print (f'Message {msg_num} is uneditable, since the message number does not exist.')
        
    elif check_thread_exists(Thread_Title) is False:
        conn.send(bytes(NO_THREAD, FORMAT))
        print (f'There is no thread corresponding to {Thread_Title}')
    
    elif find_author(Thread_Title, msg_num) != username:
        conn.send(bytes(INVALID_AUTHOR, FORMAT))
        print (f'The user cannot edit the message since he is not the author of it')
    
    else :
        edit_message(Thread_Title, username, msg_num, new_msg, t_lock)
        conn.send(bytes(MESSAGE_EDITED, FORMAT))
        print (f'Message {msg_num} successfully edited from {Thread_Title}')

            
# references to the following discussion here- 
# https://www.reddit.com/r/Python/comments/464cim/replace_a_line_in_a_txtfile/
def edit_message(Thread_Title, username, msg_num, new_msg, t_lock):
    '''Edit the given message numebr with the m essage and then update the file'''
    with t_lock:
        
        for threads in SERVER_STATE['Threads']:
            if threads['name'] == Thread_Title:
                for message in threads['messages']:
                    if message['id'] == msg_num: 
                        message['message'] = f'{msg_num} {username}: {new_msg}'
        
        new_content = read_messages(Thread_Title, t_lock)
        author = find_thread_author(Thread_Title)
        new_content['messages'].insert(0, author)
        
        with open(Thread_Title, "w") as outfile:
            outfile.write("\n".join(new_content['messages']))
            outfile.write('\n')
            
        t_lock.notify()

# #################################################################### #
#                     UPD SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #

def UPD_SERVER_STATE_UPDATE(Thread_Title, username, conn, filename):
    '''Updates the SERVER_STATE with respect to UPD and add the file to the server
    state of files'''
    with open(Thread_Title, 'a') as Thread:
        Thread.write(f'{username} uploaded {filename}\n')
    
    for thread in SERVER_STATE['Threads']:
        if thread['name'] == Thread_Title:
            thread['messages'].append({'id' : None,
            'author' : username, 'message' : f'{username} uploaded {filename}'})
    
    SERVER_STATE['Files'].append({'Thread' : Thread_Title,'filename' : filename})
    
    conn.send(bytes(UPLOAD_SUCCESSFUL, FORMAT))

def upload_file(Thread_Title, username, conn, filename, filesize):
    '''take the file from the client and write it to the thread title'''
    conn.send(bytes(WAITING_FILE_CONTENT, FORMAT))
            
    with open(Thread_Title+'-'+filename, 'wb') as UPD_file:
        data = conn.recv(MAXIMUM_LENGTH)
        totalRecv = len(data)
        UPD_file.write(data)
        
        while totalRecv < int(filesize):
            data = conn.recv(MAXIMUM_LENGTH)
            totalRecv += len(data)
            UPD_file.write(data)

    print ("Upload Complete!")
    UPD_file.close()

    UPD_SERVER_STATE_UPDATE(Thread_Title, username, conn, filename)

def UPD_process_and_exception_handle (Thread_Title, username, conn, filename, t_lock):
    '''Handles all the error cases for UPD and if they are fine then start the upload
    of the file and manges the lock so that no two threads can overwrite the file upload'''

    if check_thread_exists(Thread_Title) is False:
        conn.send(bytes(NO_THREAD, FORMAT))
        print (f'There is no thread corresponding to {Thread_Title}')
    
    else:

        with t_lock:
            
            conn.send(bytes(THREAD_EXISTS, FORMAT))
            existent_or_filesize = conn.recv(MAXIMUM_LENGTH).decode(FORMAT)

            if existent_or_filesize != FILE_NON_EXISTENT:
                
                cwd = os.getcwd()
                if check_file_exists(Thread_Title, filename):
                    conn.send(bytes(FILE_ALREADY_UPLOADED, FORMAT))
                    print (f'File {filename} already uploaded to the server..try again')
                
                else:
                    upload_file(Thread_Title, username, conn, filename, existent_or_filesize)
            
            else:
                print (f'File {filename} does not exist at the clients directory..!!')
            
            t_lock.notify()

# #################################################################### #
#                     DWN SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #

def download_file(Thread_Title, username, conn, filename, t_lock):
    '''Send the file from the current directory to the desired location by 
    reading in the contents until filesize'''

    if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == START_DOWNLOAD:
            
        with t_lock:
            
            print ('starting download..!!')
            filesize = os.path.getsize(Thread_Title+'-'+filename)
            conn.send(bytes(str(filesize), FORMAT))
            
            if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == WAITING_DOWNLOAD:

                if os.path.isfile(Thread_Title+'-'+filename):
                    
                    with open(Thread_Title+'-'+filename, 'rb') as f:
                        bytesToSend = f.read(MAXIMUM_LENGTH)
                        bytes_read = len(bytesToSend)
                        conn.send(bytesToSend)
                        
                        while bytes_read < filesize:
                            bytesToSend = f.read(MAXIMUM_LENGTH)
                            bytes_read += len(bytesToSend)
                            conn.send(bytesToSend)
        
            if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == DOWNLOAD_SUCCESSFUL:
                print (f" file {filename} successfully sent to the client..!!")

            t_lock.notify()

def DWN_process_and_exception_handle (Thread_Title, username, conn, filename, t_lock):
    '''Covers all the exception handling cases for DWN and starts the download if
    it is fine'''

    if check_thread_exists(Thread_Title) is False:
        conn.send(bytes(NO_THREAD, FORMAT))
        print (f'There is no thread corresponding to {Thread_Title}')
    
    elif check_thread_exists(Thread_Title) is True and check_file_exists(Thread_Title, filename) is False:
        conn.send(bytes(THREAD_EXISTS_FILE_NOT, FORMAT))
        print (f'The thread {Thread_Title} exisits but file {filename} does not')

    elif check_thread_exists(Thread_Title) and check_file_exists(Thread_Title, filename):
        conn.send(bytes(THREAD_FILE_EXISTS, FORMAT))
        print (f'The thread {Thread_Title} and file {filename} exists.')
        
        download_file(Thread_Title, username, conn, filename, t_lock)

# #################################################################### #
#                     RMV SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #

# Based on the discussion on this thread-
# https://stackoverflow.com/questions/2012670/deleting-files-which-start-with-a-name-python
def remove_thread(Thread_Title, username, t_lock):
    ''' Firstly remove the thread file and all the other file
    associated with it from the cwd by os.remove() and then
    mange the SERVER_STATE by removing the threads and files associated
    with it'''

    cwd = os.getcwd()
    
    for fname in os.listdir(cwd):
        if fname.startswith(Thread_Title):
            os.remove(cwd +'/'+fname)

    for threads in SERVER_STATE['Threads']:
        if threads['name'] == Thread_Title:
            SERVER_STATE['Threads'].remove(threads)
    
    for files in SERVER_STATE['Files']:
        if files['Thread'] == Thread_Title:
            SERVER_STATE['Files'].remove(files)
    

def RMV_process_and_exception_handle (Thread_Title, username, conn, t_lock):
    '''Covers all the error handling cases for RMV and if everything is fine
    then it moves ahead and execute the RMV functionality'''

    if check_thread_exists(Thread_Title) is False:
        conn.send(bytes(NO_THREAD, FORMAT))
        print (f'There is no thread corresponding to the {Thread_Title}')
        
    else:
        
        with t_lock:
            
            if check_thread_exists(Thread_Title) is True and check_author_thread(Thread_Title, username) is False:
                print ('thread exists but the author of the thread is wrong..!!')
                conn.send(bytes(THREAD_EXISTS_AUTHOR_WRONG, FORMAT))
            
            elif check_thread_exists(Thread_Title) and check_author_thread(Thread_Title, username):
                conn.send(bytes(THREAD_AUTHOR_EXISTS, FORMAT))

                if conn.recv(MAXIMUM_LENGTH).decode(FORMAT) == START_REMOVING:

                    remove_thread(Thread_Title, username, t_lock)
                    print (f'Thread {Thread_Title} and its associated fields removed from the server')
                    conn.send(bytes(THREAD_REMOVED, FORMAT))
            
            t_lock.notify()


# #################################################################### #
#                     SHT SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #

def Initiate_SHT(conn):
    '''When shutdown is initiated remove all the 
    files from the current working directory of server
    and then clear all the other data structures associated with it'''

    conn.send(bytes(INITIATING_SHUTDOWN, FORMAT))
    
    cwd = os.getcwd()
    for fname in os.listdir(cwd):
        if fname == 'credentials.txt':
            os.remove(cwd +'/'+fname)
        for threads in SERVER_STATE['Threads']:
            if fname.startswith(threads['name']):
                os.remove(cwd +'/'+fname)
    
    SERVER_STATE['Threads'].clear()
    SERVER_STATE['Files'].clear()

# #################################################################### #
#                     LST SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #

def list_messages(t_lock):
    '''List the name of all the active threads at the moment'''
    with t_lock:
        
        Active_threads = {'Threads' : []}
        for thread in SERVER_STATE['Threads']:
            Active_threads['Threads'].append(thread['name'])
        t_lock.notify()
    
    return Active_threads

# #################################################################### #
#                     RDT SPECIFIC HELPER FUNCTIONS                    #
# #################################################################### #

def read_messages(Thread_Title, t_lock):
    '''Reads the messages from the particular thread and return them'''
    with t_lock:
        
        Thread_msgs = {'messages' : []}
        
        for threads in SERVER_STATE['Threads']:
            if threads['name'] == Thread_Title:
                for message in threads['messages']:
                    Thread_msgs['messages'].append(message['message'])
    
        t_lock.notify()

    return Thread_msgs

# #################################################################### #
#                     OTHER SPECIFIC HELPER FUNCTIONS                  #
# #################################################################### #

def get_command_args (command):
    '''get the list of all the command line args given'''
    command_args = command.split()
    return command_args

def last_msg_num(Thread_Title):
    ''' Finds the last msg_num which is not 
    None to find the last num of message sent'''
    last_msg_num = 0
    for thread in SERVER_STATE['Threads']:
        if thread['name'] == Thread_Title:
            for message in thread['messages']:
                if message['id'] != None:
                    last_msg_num = message['id']
    return last_msg_num

def find_num_msgs(Thread_Title):
    ''' Find the number of messages added in the thread
    does not take into consideration file uploads'''

    for thread in SERVER_STATE['Threads']:
        if thread['name'] == Thread_Title: 
            num_messages = last_msg_num(Thread_Title)
    
    return num_messages
        
def find_author(Thread_Title, msg_num):
    ''' Find the author of the current msg_num
    in the thread'''

    for thread in SERVER_STATE['Threads']:
        if thread['name'] == Thread_Title:
            for message in thread['messages']:
                if message['id'] == msg_num:
                    author = message['author']
    
    return author

def check_thread_exists(Thread_Title):
    '''Check if the thread is an Active thread in the SERVER_STATE['threads']'''

    for threads in SERVER_STATE['Threads']:
        if threads['name'] == Thread_Title:
            return True
    return False

def check_file_exists(Thread_Title, filename):
    '''Check if the given file exists in the SERVER_STATE['files']'''
    for files in SERVER_STATE['Files']:
        if files['Thread'] == Thread_Title and files['filename'] == filename:
            return True
    
    return False

def check_author_thread(Thread_Title, username):  
    '''Check if the given user is the author of the thread'''
    for threads in SERVER_STATE['Threads']:
        if threads['name'] == Thread_Title:
            if threads['creator'] == username:
                return True
    return False

def find_thread_author(Thread_Title):
    '''Gives the author of the thread'''
    for threads in SERVER_STATE['Threads']:
        if threads['name'] == Thread_Title:
            return threads['creator']
                


