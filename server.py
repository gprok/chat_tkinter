from dotenv import load_dotenv
import os
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

load_dotenv()
clients = []
ip = os.getenv('SERVER_IP')
port = int(os.getenv('SERVER_PORT'))


def remove_client(c_conn, c_addr):
    clients.remove((c_conn, c_addr))


def broadcast(message):
    for client in clients:
        client[0].send(message.encode('utf-8'))


def receive_from_client_thread(c_name, c_conn, c_addr):
    while True:
        data = c_conn.recv(1024)
        message = data.decode("utf-8")
        if message == "exit":
            message = c_name + " left chat"
            print(message)
            remove_client(c_conn, c_addr)
            broadcast(message)
            break
        message = c_name + ": " + message
        print(message)
        broadcast(message)


server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((ip, port))
server_socket.listen()
print("Server started at", ip, ":", port)

while True:
    print("Waiting for connection...")
    connection, client_address = server_socket.accept()
    print("Connection from", client_address)
    clients.append((connection, client_address))
    name_bytes = connection.recv(1024)
    name = name_bytes.decode("utf-8")
    msg = name + " joined the chat"
    broadcast(msg)
    th = Thread(target=receive_from_client_thread, args=(name, connection, client_address))
    th.start()

