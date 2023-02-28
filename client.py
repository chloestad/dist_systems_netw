# Importing modules that will be used.
import socket
import threading
import tkinter as tk
from tkinter import font
from tkinter import scrolledtext
from tkinter import messagebox
from turtle import width
from matplotlib.pyplot import connect
from pyrsistent import b 

''''
We need a client script that connects to the server.
'''

#----------------------- GLOBAL VARIABLES -----------------------#
# We create global variables that are constants for the host and port.
HOST = '127.0.0.1'
PORT = 1234

# Fonts and colors
DARK_GREY = '#5A5A5A'
LIGHT_GREY = '#D3D3D3'
WHITE = 'white'
LIGHT_BLUE = '#ADD8E6'
FONT = ('Arial', 16)
BUTTON_FONT = ('Arial', 14)
SMALL_FONT = ('Arial', 12)  

# We create the client socket class object.
# Notice that we have the same configuration that in server,
# this is so that the server and client can connect. 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#-------------------- Creating client interface --------------------#

# FUNCTIONS
def update_messages(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect(): 
    # We want to connect to the server.
    # We use a try block in case the server is down.
    try:
        client.connect((HOST, PORT))
        print(f'Successfully connected to server.')
        update_messages('[SERVER] successfully connected to the server')
    except:
        messagebox.showerror('Unable to connect to server', f'Unable to connect to server {HOST} {PORT}')
    
    username = username_textbox.get()
    if username:
        client.sendall(username.encode())

    else:
        messagebox.showerror('Invalid username','Username cannot be empty.')
    
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message:
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))

    else:
        messagebox.showerror('Empty message.', 'Message cannot be empty.')


root = tk.Tk()
# Size of the window in pixels.
root.geometry('600x600')
# Title.
root.title('Client Chat')
# We want to always keep the same size.
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

# We want to devide in smaller areas (3 frames).
top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=LIGHT_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# WIDGETS
# Labels
username_label = tk.Label(top_frame, text='Write your username:', font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

# Textbox
username_textbox = tk.Entry(top_frame, font=FONT, bg=LIGHT_GREY, fg=DARK_GREY, width=23)
username_textbox.pack(side=tk.LEFT)

# Join button
username_button = tk.Button(top_frame, text='Join!', font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_GREY, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

# Message textbox and button
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=LIGHT_GREY, fg=DARK_GREY, width=50)
message_textbox.pack(side=tk.LEFT, padx=10)
message_button = tk.Button(bottom_frame, text='Send', font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_GREY, command=send_message)
message_button.pack(side=tk.LEFT, padx=15)

# Box that contains the texts
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=LIGHT_GREY, fg=DARK_GREY, width=82, height=37)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)
#--------------------------------------------------------------------# 

def listen_for_messages_from_server(client):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message:
            username = message.split('~')[0]
            content = message.split('~')[1]

            update_messages(f'[{username}] {content}')

        else:
            messagebox.showerror('Error','Message recevied from client is empty.')

def main():

    root.mainloop()

if __name__ == '__main__':
    main()