'''
Server
It recieves messages from one user and broadcasts it to all users.
Adds new users.
Broadcasts a message when a user joins or leaves.

'''

import socket
import threading
HOST="127.0.0.1" #local host
PORT = 50000

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()
clients = []  #keeps track of active users
nicknames= [] #users with their corresponding username
adresses = []

def broadcast(message):
    ''' broadcasts the message to all users
        argument: message
    '''
    for client in clients:
        client.send(message)
    
def handle(client):
    while True:
        try:
            message = client.recv(1024) # constantly recieves messages from users
            if message.decode('ascii').strip().lower().endswith('exit'):
                ''' disconnects the user once he input "exit" 
                    and announces it.
                '''
                index = clients.index(client)
                nickname = nicknames[index]
                client.close() #breaks the connection of user with the server.
                clients.remove(client)
                broadcast(f"{nickname} left the chat!".encode("ascii"))
                print(f"{str(adresses[index])} disconnected") 
                nicknames.remove(nickname)
                break
            else:
                broadcast(message) #broadcasting


                 
        except:
            ''' error handling'''
            index = clients.index(client)
            nickname = nicknames[index]
            clients.remove(client)
            client.close()
            broadcast(f"{nickname} left the chat!".encode("ascii")) 
            
            nicknames.remove(nickname)
            break

def recieve():
    ''' handles the new users.
        forms a new socket/connection with the server.
        Adds the user to the list.
    '''

    while True:
        client,adr = s.accept() #forms a new connection
        client.send("NICK".encode("ascii")) #sends a keyword for new users
        nickname = client.recv(1024).decode("ascii")
        clients.append(client)
        nicknames.append(nickname)
        adresses.append(adr)
        print(f"{str(adr)} connected")
        broadcast(f"{nickname} joined the chat!".encode("ascii")) # announces the new user
        threading.Thread(target=handle, args=(client,)).start() # makes both handle and recieve functions run simultaneously
print("System is running...")
recieve()



