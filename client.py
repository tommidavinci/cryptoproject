#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = input('Enter host: ')
if not HOST:
    HOST = "localhost"
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

msg = client_socket.recv(BUFSIZ).decode("utf8")
print(msg)
name = input()
client_socket.send(bytes(name, "utf8"))

while True:
    try:
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        print(msg)
        if msg == "quit":
            print("closing...")
            client_socket.close()
            break
        selection = input()
        client_socket.send(bytes(selection, "utf8"))

    except OSError:  # Possibly client has left the chat.
        break



