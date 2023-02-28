# Importing modules that will be used.
from email import message
from pydoc import cli
import socket # for the main communication part
import threading

from aiohttp import client
from matplotlib.style import use 

''''
We need a server that is able to listen to client connections
'''

# We create global variables that are constants for the host and port.
HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users.

# Function to listen for any upcomming messages from a client.
def listen_for_messages(client, username):
    
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message:
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
            
        else:
            print(f'The message sent from client {username} is empty.')


# Function to send message to a single client.
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function so send any new message to all clients that
# are currently connected to the server.
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client.
def client_handler(client):
    
    # Server will listen for client message taht will contain
    # the username.
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username:
            active_clients.append((username, client))
            prompt_message = 'SERVER~' + f'{username} just entered the chat.'
            send_messages_to_all(prompt_message)
            break

        else:
            print('Client username is empty.')
    
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


def main():
    # We create the server socket class object.
    # AF_INET means that we will use IPv4 addresses.
    # SOCK_STREAM menas we are going to use TCP packets for communication.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # We want to bind the server to a host and port. So we 
    # create a try catch block.
    try:
        # Provide the server with an address in the form of host IP and port.
        server.bind((HOST, PORT))
        print(f'Running the server on {HOST} {PORT}')
    except:
        print(f'Unable to bind to host {HOST} and port {PORT}')
    
    # Set server limit (client maximum of 5 connections -constant-).
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections.
    while 1:
        client, address = server.accept()
        print(f'Successfully connected to client {address[0]} {address[1]}')

        # To call the client handler function, we will use threading.
        threading.Thread(target=client_handler, args=(client, )).start()
    


if __name__ == '__main__':
    main()