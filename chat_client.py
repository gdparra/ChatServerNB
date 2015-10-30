# chat_client.py

import sys
import socket
import select
 
def chat_client():
    if(len(sys.argv) < 4) :
        print 'Usage : python chat_client.py hostname port key'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    key  = int(sys.argv[3])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('[Me] '); sys.stdout.flush()
    
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    translated = ''
                    for symbol in data:
                        if symbol.isalpha():
                            num = ord(symbol)
                            num += -key
                
                            if symbol.isupper():
                                if num > ord('Z'):
                                    num -= 26
                                elif num < ord('A'):
                                    num += 26
                            elif symbol.islower():
                                if num > ord('z'):
                                    num -= 26
                                elif num < ord('a'):
                                    num += 26
                                    
                            translated += chr(num)
                        else:
                            translated += symbol
                    data = translated                
                    #-------------------------------                    
                    #print data
                    sys.stdout.write(data[24:])
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                                
                # Encrypt
                translated = ''
                for symbol in msg:
                    if symbol.isalpha():
                        num = ord(symbol)
                        num += key
            
                        if symbol.isupper():
                            if num > ord('Z'):
                                num -= 26
                            elif num < ord('A'):
                                num += 26
                        elif symbol.islower():
                            if num > ord('z'):
                                num -= 26
                            elif num < ord('a'):
                                num += 26
                                
                        translated += chr(num)
                    else:
                        translated += symbol
                msg = translated                
                #-------------------------------
                
                s.send(msg)
                sys.stdout.write('[Me] '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())