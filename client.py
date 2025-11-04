'''
Client
sends the user input as messages to the server.
recieves the messages from serves and prints it on the terminal
'''

import socket
import threading
import sys
HOST = '127.0.0.1'
PORT = 50000
nickname = input("Enter your nickname: ")
doesExist = True #flag


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))


def read():
    ''' recieves the message from the server and prints it on the terminal '''
    
    while doesExist:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICK": #accepts the keyword given out by server and asks the user for a nickname
                client.send(nickname.encode("ascii"))
            elif(message.partition(":")[0]== nickname):
                print("Me: " + message.partition(":")[2])
            else:
                print(message)
        except:
            ''' error handling '''
            client.close()
            sys.exit()
            break

def write():
    ''' sends out the user input to the server '''
    while True:
        try:
            message = (f"{nickname}: {input("")}").encode("ascii") #user input
            if message.decode('ascii').strip().lower().endswith('exit'):
                ''' checks if the user wants to exit '''
                print(f"Goodbye {nickname}") # exit message
                client.send('exit'.encode("ascii"))
                client.close()
                doesExist = False
                sys.exit()
                
            else:
                client.send(message)
        except:
            ''' error handling '''
            client.close()
            sys.exit()
            break

threading.Thread(target=read).start()
threading.Thread(target=write).start()







