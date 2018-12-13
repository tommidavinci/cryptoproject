import nacl.secret
import nacl.utils
import nacl.signing
import pickle
from socket import AF_INET, socket, SOCK_STREAM
from nacl.public import PrivateKey, Box, PublicKey
from nacl.signing import VerifyKey
from threading import Thread
from moviestore import MovieStore
from movieview import MovieView
from moviecontroller import MovieController
from db import DB
from encryption_functions import sign_and_encrypt, decrypt_and_verify


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        
        client.send(pickle.dumps([bytes(pkserver), bytes(server_verify_key)]))
        combined_key = pickle.loads(client.recv(BUFSIZ))
        client_publickey = PublicKey(combined_key[0])
        print("Received client public key: ")
        print(client_publickey)
        client_verify_key = VerifyKey(combined_key[1])
        print("Received client verify key: ")
        print(client_verify_key)
        server_client_box = Box(skserver, client_publickey)

        nonce = nacl.utils.random(Box.NONCE_SIZE)
        encrypted = server_client_box.encrypt(symmetric_secret_key, nonce)
        client.send(encrypted)

        encrypted = sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, "Greetings from the cave! Now type your name and press enter!")
        client.send(encrypted)

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_verify_key)).start()


def handle_client(client, client_verify_key):  # Takes client socket as argument.
    """Handles a single client connection."""
    name_encrypted = client.recv(BUFSIZ)
    name = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, name_encrypted)

    clients[client] = name
    quit = False
    while quit == False:
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        welcome += '\nBelow you can see a list of operation you can perform:'
        welcome += '\n1. Search for a movie'
        welcome += '\n2. List all the movies that you have rated or reviewed'
        welcome += '\n3. List all the movies that has similar genres with a given movie'
        welcome += '\n4. List all the movies that you might interested in'
        welcome += '\n5. Rate a movie'
        welcome += '\n6. Edit your rate for a movie'
        welcome += '\n7. Delete your rate for a movie'
        welcome += '\n8. Create a review for a movie'
        welcome += '\n9. Edit your review for a movie'
        welcome += '\n10. Delete your review for a movie'
        welcome += '\n11. Create a user (Admin right)'
        welcome += '\nEnter your choice (number) - type "quit" to exit: '

        #You can add as many functionalities as you want

        client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, welcome))

        msg = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
        while True:
            if msg == '1':
                client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, "Please enter the movie name you want to search: "))
                search_string = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                result = movie_controller.search_movie(search_string)
                result += '\nPlease enter the movie name you want to search or type "back" to return to Home: '
                client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, result))

                next_search = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                while next_search != 'back':
                    result = movie_controller.search_movie(next_search)
                    result += '\nPlease enter the movie name you want to search or type "back" to return to Home: '
                    client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, result))
                    next_search = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                break
            elif msg == '2':
                result = movie_controller.get_rated_movies(1)
                result += '\nSend any key to return to Home'
                client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, result))
                back = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                break
            elif msg == '3':
                client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, "Please enter a movie ID you want to find other similar movies to: "))
                search_string = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                result = movie_controller.get_similar_movies(search_string)
                result += '\nPlease enter a movie ID you want to find other similar movies to' \
                          ' or type "back" to return to Home: '
                client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, result))
                next_search = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                while next_search != 'back':
                    result = movie_controller.get_similar_movies(next_search)
                    result += '\nPlease enter a movie ID you want to find other similar movies to' \
                              ' or type "back" to return to Home: '
                    client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, result))
                    next_search = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                break
            elif msg == '4':
                result = movie_controller.get_interested_movies(1)
                result += '\nSend any key to return to Home'
                client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, result))
                back = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, client.recv(BUFSIZ))
                break
            elif msg == 'quit':
                client.send(sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, "quit"))
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

skserver = PrivateKey.generate()
pkserver = skserver.public_key
print(pkserver)
server_signing_key = nacl.signing.SigningKey(bytes(skserver))
server_verify_key = server_signing_key.verify_key
print(server_verify_key)
symmetric_secret_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
symmetric_secret_key_box_server = nacl.secret.SecretBox(symmetric_secret_key)

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