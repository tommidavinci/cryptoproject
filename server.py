#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the movie database! Now type your username and press enter! We are very secure!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    clients[client] = name

    while True:
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        welcome += '\nBelow you can see a list of operation you can perform:'
        welcome += '\n1. Search for a movie'
        welcome += '\n2. List all the movies that you have rated'
        welcome += '\n3. List all the movies that has similar genres with a given movie'
        welcome += '\n4. List all the movies that he might interested in\n'
        welcome += '\nEnter your choice (number) - type "quit" to exit: '
        client.send(bytes(welcome, "utf8"))

        msg = client.recv(BUFSIZ).decode("utf-8")
        while msg != 'quit':
            if msg == '1':
                client.send(bytes("Please enter the movie name you want to search: ", "utf8"))
                search_string = client.recv(BUFSIZ).decode("utf8")
                result = '1 match found with ' + search_string + ': Id: 101 - The Avengers'
                result += '\nPlease enter the movie name you want to search or type Back to return to Home: '
                client.send(bytes(result, "utf8"))
                back = client.recv(BUFSIZ).decode("utf8")
                while back != 'back':
                    result = '1 match found with ' + search_string + ': Id: 101 - The Avengers'
                    result += '\nPlease enter the movie name you want to search or type Back to return to Home: '
                    client.send(bytes(result, "utf8"))
                    back = client.recv(BUFSIZ).decode("utf8")
                break
            elif msg == '2':
                result = "Here is the list of movies you have rated: "
                result += '\nForest Gump - 4.5'
                result += '\nA Star is born - 4.0'
                result += '\nWall Street - 5.0'
                result += '\nFriends - 5.0'
                result += '\nSend any key to return to Home'
                client.send(bytes(result, "utf8"))
                back = client.recv(BUFSIZ).decode("utf8")
                break
            elif msg == '3':
                client.send(bytes("Please enter a movie ID you want to find other similar movies to: ", "utf8"))
                search_string = client.recv(BUFSIZ).decode("utf8")
                result = '2 match found with ' + search_string + ': '
                result += '\nId: 101 - The Avengers. Genres: Action | Comedy'
                result += '\nId: 87 - 007. Genres: Action | Comedy'
                result += '\nPlease enter a movie ID you want to find other similar movies to' \
                          ' or type Back to return to Home: '
                client.send(bytes(result, "utf8"))
                back = client.recv(BUFSIZ).decode("utf8")
                while back != 'back':
                    result = '2 match found with ' + search_string + ': '
                    result += '\nId: 101 - The Avengers. Genres: Action | Comedy'
                    result += '\nId: 87 - 007. Genres: Action | Comedy'
                    result += '\nPlease enter a movie ID you want to find other similar movies to' \
                              ' or type Back to return to Home: '
                    client.send(bytes(result, "utf8"))
                    back = client.recv(BUFSIZ).decode("utf8")
                break
            elif msg == '4':
                result = "Here is the list of movies you might be interested in: "
                result += '\nForest Gump - Proximity: 4.6'
                result += '\nA Star is born - Proximity: 4.6'
                result += '\nWall Street - Proximity: 4.6'
                result += '\nFriends - Proximity: 4.6'
                result += '\nSend any key to return to Home'
                client.send(bytes(result, "utf8"))
                back = client.recv(BUFSIZ).decode("utf8")
                break
            else:
                break
        client.send(bytes('quit', "utf8"))
        client.close()
        del clients[client]
        print(clients)
        break

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()