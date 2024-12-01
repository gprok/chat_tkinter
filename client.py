from tkinter import Tk, Button, Listbox, Entry, Frame, END
from dotenv import load_dotenv
import os
import sys
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def receive_from_server_thread():
    while True:
        msg_bytes = client_socket.recv(1024)
        msg = msg_bytes.decode('utf-8')
        listbox.insert(END, msg)


def send_message_to_server():
    msg = entry.get()
    if len(msg) > 0:
        msg_bytes = msg.encode('utf-8')
        client_socket.send(msg_bytes)
        entry.delete(0, END)
    if msg == 'exit':
        sys.exit()


def enter_pressed(event):
    send_message_to_server()


def window_closing():
    msg = 'exit'
    msg_bytes = msg.encode('utf-8')
    client_socket.send(msg_bytes)
    sys.exit()


load_dotenv()
ip = os.getenv('SERVER_IP')
port = int(os.getenv('SERVER_PORT'))

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((ip, port))

name = sys.argv[1]
name_bytes = name.encode('utf-8')
client_socket.send(name_bytes)

window = Tk()
window.title("CHAT - " + name)
window.geometry('270x380')
window.bind('<Return>', enter_pressed)

listbox = Listbox(window, height=20)
listbox.grid(row=0, column=0)

frame = Frame(window)
entry = Entry(frame, width=20)
entry.grid(row=0, column=0)
button = Button(frame, text=' > ', command=send_message_to_server)
button.grid(row=0, column=1)
frame.grid(row=1, column=0)

th = Thread(target=receive_from_server_thread)
th.start()

window.protocol("WM_DELETE_WINDOW", window_closing)
window.mainloop()
