# ##############################################################################################################################################
#                                        DIGITAL FORUM PROTOCOL(DFP) LAYOUT/ MESSAGES FOR INTERACTION                                          #  
# ##############################################################################################################################################


# #################################################################### #
#                     GENERAL CONSTANTS                                #  
# #################################################################### #
MAXIMUM_LENGTH = 2048
FORMAT = 'utf-8'
SPECIAL_PRIVELAGES_PORT = 1024
UPDATE_INTERVAL = 0.4

# #################################################################### #
#               AUTHENTICATION REALTED DFP CONSTANTS                   #  
# #################################################################### #

NEW_PASSWORD = 'DFP 900, new password required for the user'
EXPECTING_PASSWORD = 'DFP 800, expecting a password'
USER_AUTHORISED = 'DFP 824, congratulations the user is authorised.'
USERNAME_REQUIRED = 'DFP 1000, username for the current user is required.'
PASSWORD_REQUIRED = 'DFP 1021, password required for the current user'
USERNAME_ALREADY_LOGGEDIN = 'DFP 6529 username already in the logged in session'
NEW_USER_ADDED = 'DFP 9776 new user successfully added'
USER_UNAUTHORISED = 'DFP 78 USER IS STILL UNAUTHORISED'
AUTHORIZATION_COMPLETE = 'DFP 99 AUTHORIZATION COMPLETE START FORUM'

# #################################################################### #
#               FORUM INTERACTION REALTED DFP CONSTANTS                #  
# #################################################################### #
FORUM_START = 'DFP 2024 INTERACTION WITH FORUM BEGINS'
INVALID_COMMAND = 'DFP 1024 THE COMMAND ENTERED IS NOT A VALID COMMAND'
COMMAND_FOUND = 'DFP 2020 VALID COMMAND'
PROCESS_COMMAND = 'DFP 132 processing the current command'

# #################################################################### #
#                     INVALID ARGUMENTS COMMMANDS                      #  
# #################################################################### #
INVALID_CRT = 'Invalid arguments. USAGE CRT <Threadtitle>'
INVALID_MSG = 'Invalid arguments. USAGE MSG <Threadtitle> <message>'
INVALID_DLT = 'Invalid arguments. USAGE DLT <Threadtitle> <message_number(int)>'
INVALID_EDT = 'Invalid arguments. USAGE EDT <Threadtitle> <message_number(int)> <message>'
INVALID_LST = 'Invalid arguments. USAGE LST' 
INVALID_RDT = 'Invalid arguments. USAGE RDT <Threadtitle>'
INVALID_UPD = 'Invalid arguments. USAGE UPD <Threadtitle> <filename>'
INVALID_DWN = 'Invalid arguments. USAGE DWN <Threadtitle> <filename>'
INVALID_RMV = 'Invalid arguments. USAGE RMV <Threadtitle> <filename>'
INVALID_XIT = 'Invalid arguments. USAGE XIT'
INVALID_SHT = 'Invalid arguments. USAGE SHT <admin_password>'

# #################################################################### #
#                CRT  REALTED DFP CONSTANTS                            #  
# #################################################################### #

THREAD_EXISTS = 'DFP 1020 THREAD EXISTS, CREATE ANOTHER THREAD'
THREAD_CREATED = 'DFP 2025 THREAD CREATED, NOW START ADDING MESSAGES'

# #################################################################### #
#                MSG  REALTED DFP CONSTANTS                            #  
# #################################################################### #

MESSAGE_ADDED = 'DFP 1060 MESSAGE ADDED IN THE CURRENT THREAD.'
THREAD_DOES_NOT_EXIST = 'DFP 1050 MESSAGE CAN''T BE ADDED'

# #################################################################### #
#                  DLT  REALTED DFP CONSTANTS                          #  
# #################################################################### #

MESSAGE_UNDELETABLE = 'DFP 1220 MESSAGE CAN''T BE DELETED'
MESSAGE_DELETED = 'DFP 9090 the desired message is deleted.'
INVALID_MESSAGE_NUMBER = 'DFP 9430 the message number sent does not correspond to a message on the thread'

# #################################################################### #
#                  EDT  REALTED DFP CONSTANTS                          #  
# #################################################################### #

MESSAGE_UNEDITABLE = 'DFP 3200 MESSAGE CAN''T BE EDITED'
MESSAGE_EDITED = 'DFP 1300 the desired message number has been edited'

# #################################################################### #
#                  LST  REALTED DFP CONSTANTS                          #  
# #################################################################### #

NO_ACTIVE_THREADS = 'DFP 9999 There are no active threads to be listed.'

# #################################################################### #
#                  RDT  REALTED DFP CONSTANTS                          #  
# #################################################################### #
NO_THREAD = 'DFP 1778 There is no thread corresponding to the desired thread.'

# #################################################################### #
#                  UPD  REALTED DFP CONSTANTS                          #  
# #################################################################### #
WAITING_FILE_CONTENT = 'DFP 700 Waiting for the file contents to be uploaded.'
UPLOAD_SUCCESSFUL = 'DFP 2221 The file contents have been transferred succesfully from the client'
FILE_ALREADY_UPLOADED = 'DFP 2090 The file has already been uploaded to the thread.'
FILE_NON_EXISTENT = 'DFP 6662 the file does not exists in the clients directory'

# #################################################################### #
#                COMMON UPD AND DWN REALTED DFP CONSTANTS              #  
# #################################################################### #
THREAD_FILE_EXISTS = 'DFP 1321 The Thread requested and the file requested already exists'
THREAD_EXISTS_FILE_NOT ='DFP 7777 the thread requested exits but the file does not'

# #################################################################### #
#                  DWN REALTED DFP CONSTANTS                           #  
# #################################################################### #
START_DOWNLOAD = 'DFP 3030 start the download of the desired file in the desired thread'
WAITING_DOWNLOAD = 'DFP 9097 the client is waiting for the download of the file'
DOWNLOAD_SUCCESSFUL = 'DFP 5643 The download of the file is successful'

# #################################################################### #
#                  RMV  REALTED DFP CONSTANTS                          #  
# #################################################################### #
THREAD_AUTHOR_EXISTS = 'DFP 4333 The thread exists and the username given is same as the author of the thread'
START_REMOVING = 'DFP 1289 start removing the elements from the thread'
THREAD_REMOVED = 'DFP 2378  Successfully removed everything from the thread includingits associated files'
THREAD_EXISTS_AUTHOR_WRONG = 'The thread exists but the given user is not the auhor of the thread'
INVALID_AUTHOR = 'DFP 1278 the user is no the author of the given message'

# #################################################################### #
#                  XIT  REALTED DFP CONSTANTS                          #  
# #################################################################### #
SERVER_STATE_UPDATED_XIT = 'DFP 2345 the current client is removed from server''s list of active users' 

# #################################################################### #
#                  SHT  REALTED DFP CONSTANTS                          #  
# #################################################################### #
INVALID_ADMIN_PASSWORD = 'DFP 1243 the password entered does not match the admin password.'
INITIATING_SHUTDOWN = 'DFP 7410 shutting down the server and removing all the threads.'

# #################################################################### #
#       BACKGROUND THREAD ALIVE SHT REALTED DFP CONSTANTS              #  
# #################################################################### #

RESPONSE_REQUIRED ='DFP 2327 user requires a response'
ALIVE = 'DFP 7777 the server is alive'
