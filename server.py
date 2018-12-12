#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from moviestore import MovieStore
from movieview import MovieView
from moviecontroller import MovieController
from db import DB


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
    quit = False
    while quit == False:
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        welcome += '\nBelow you can see a list of operation you can perform:'
        welcome += '\n1. Search for a movie'
        welcome += '\n2. List all the movies that you have rated'
        welcome += '\n3. List all the movies that has similar genres with a given movie'
        welcome += '\n4. List all the movies that he might interested in\n'
        welcome += '\nEnter your choice (number) - type "quit" to exit: '
        client.send(bytes(welcome, "utf8"))

        msg = client.recv(BUFSIZ).decode("utf-8")
        while True:
            if msg == '1':
                client.send(bytes("Please enter the movie name you want to search: ", "utf8"))
                search_string = client.recv(BUFSIZ).decode("utf8")
                result = movie_controller.search_movie(search_string)
                result += '\nPlease enter the movie name you want to search or type "back" to return to Home: '
                client.send(bytes(result, "utf8"))
                next_search = client.recv(BUFSIZ).decode("utf8")
                while next_search != 'back':
                    result = movie_controller.search_movie(next_search)
                    result += '\nPlease enter the movie name you want to search or type "back" to return to Home: '
                    client.send(bytes(result, "utf8"))
                    next_search = client.recv(BUFSIZ).decode("utf8")
                break
            elif msg == '2':
                result = movie_controller.get_rated_movies(1)
                result += '\nSend any key to return to Home'
                client.send(bytes(result, "utf8"))
                back = client.recv(BUFSIZ).decode("utf8")
                break
            elif msg == '3':
                client.send(bytes("Please enter a movie ID you want to find other similar movies to: ", "utf8"))
                search_string = client.recv(BUFSIZ).decode("utf8")
                result = movie_controller.get_similar_movies(search_string)
                result += '\nPlease enter a movie ID you want to find other similar movies to' \
                          ' or type "back" to return to Home: '
                client.send(bytes(result, "utf8"))
                next_search = client.recv(BUFSIZ).decode("utf8")
                while next_search != 'back':
                    result = '2 match found with ' + search_string + ': '
                    result += movie_controller.get_similar_movies(next_search)
                    result += '\nPlease enter a movie ID you want to find other similar movies to' \
                              ' or type "back" to return to Home: '
                    client.send(bytes(result, "utf8"))
                    next_search = client.recv(BUFSIZ).decode("utf8")
                break
            elif msg == '4':
                result = movie_controller.get_interested_movies(1)
                result += '\nSend any key to return to Home'
                client.send(bytes(result, "utf8"))
                back = client.recv(BUFSIZ).decode("utf8")
                break
            elif msg == 'quit':
                client.send(bytes('quit', "utf8"))
                client.close()
                del clients[client]
                print(clients)
                quit = True
                break
            else:
                break


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

db = DB()
movie_store = MovieStore(db)
movie_view = MovieView()
movie_controller = MovieController(movie_store, movie_view)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()