import nacl.secret
import nacl.utils
import nacl.signing
import pickle
import os
from socket import AF_INET, socket, SOCK_STREAM
from nacl.public import PrivateKey, Box, PublicKey
from nacl.signing import VerifyKey
from threading import Thread
from models.moviestore import MovieStore
from views.movieview import MovieView
from controllers.moviecontroller import MovieController
from models.userstore import UserStore
from views.userview import UserView
from controllers.usercontroller import UserController
from database.db import DB
from database.Neo4J.graphdb import neo4jDB
from common_functions import sign_and_encrypt, decrypt_and_verify


#################################################### Sets up handling for incoming clients
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        
        client.send(pickle.dumps([bytes(pkserver), bytes(server_verify_key)]))
        combined_key = pickle.loads(client.recv(BUFSIZ))
        client_publickey = PublicKey(combined_key[0])

        client_verify_key = VerifyKey(combined_key[1])
        server_client_box = Box(skserver, client_publickey)

        symmetric_secret_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        symmetric_secret_key_box_server = nacl.secret.SecretBox(symmetric_secret_key)
        
        nonce = nacl.utils.random(Box.NONCE_SIZE)
        encrypted = server_client_box.encrypt(symmetric_secret_key, nonce)
        client.send(encrypted)

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_verify_key, symmetric_secret_key_box_server)).start()

#################################################### Handles a single client connection
def handle_client(client, client_verify_key, box):  # Takes client socket as argument.
    quit = False
    userId = 0
    userName = "Anon"
    #################################################### Login Screen
    while quit == False:
        client.send(sign_and_encrypt(box, server_signing_key, '1. Login\n2. Signup:\n3. Anon'))
        msg = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))

        if msg == '3': #################################################### Use Application as Anonymous
            quit = True
        else:
            client.send(sign_and_encrypt(box, server_signing_key, 'Username: '))
            username = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
            client.send(sign_and_encrypt(box, server_signing_key, 'Password: '))
            password = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))

            if msg == '1': #################################################### Login
                result = user_controller.login(username, password)
                if result is not None:
                    userId = result
                    userName = username
                    quit = True
                else:
                    client.send
                    
            elif msg == '2': #################################################### Signup
                result = user_controller.signup(username, password)
                if result is not None:
                    userId = result
                    userName = username
                    quit = True

    #################################################### Home Page (Server functionality)
    quit = False
    while quit == False:
        welcome = ""
        if userId == 0:
            welcome = movie_view.print_anon_functions(userName)
        else:
            welcome = movie_view.print_user_functions(userName)
        client.send(sign_and_encrypt(box, server_signing_key, welcome))
        msg = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
        while True:
            if msg == '1': #################################################### Search for a movie
                client.send(sign_and_encrypt(box, server_signing_key, "Please enter the movie name you want to search:\nTo specify year, use --year\nExample: star wars --year 2018 "))
                search_string = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                result = movie_controller.search_movie(search_string)
                result += '\nPlease enter the movie name you want to search or type "back" to return to Home: '
                client.send(sign_and_encrypt(box, server_signing_key, result))
                next_search = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                while next_search != 'back':
                    result = movie_controller.search_movie(next_search)
                    result += '\nPlease enter the movie name you want to search or type "back" to return to Home: '
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    next_search = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                break

            elif msg == '2': #################################################### Find movies similar to a movie
                client.send(sign_and_encrypt(box, server_signing_key, "Please enter a movie ID you want to find other similar movies to: "))
                search_string = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                result = movie_controller.get_similar_movies_by_genre(search_string)
                result += '\nPlease enter a movie ID you want to find other similar movies to' \
                          ' or type "back" to return to Home: '
                client.send(sign_and_encrypt(box, server_signing_key, result))
                next_search = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                while next_search != 'back':
                    result = movie_controller.get_similar_movies_by_genre(next_search)
                    result += '\nPlease enter a movie ID you want to find other similar movies to' \
                              ' or type "back" to return to Home: '
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    next_search = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                break
            #################################################### User only functions
            if userId > 0:
                ######### Ratings

                if msg == '3': #################################################### Get movies user might be interested in by Precise algorithm
                    result = movie_controller.get_precise_interested_movies(userId)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                if msg == '4': #################################################### Get movies user might be interested in by Quick algorithm
                    result = movie_controller.get_quick_interested_movies(userId)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                elif msg == '5': #################################################### Get movies rated by logged in user
                    result = movie_controller.get_rated_movies(userId)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                elif msg == '6': #################################################### Rate a movie
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    client.send(sign_and_encrypt(box, server_signing_key, 'Rating: '))
                    rating = float(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    result = movie_controller.set_movie_rating(userId, movie_id, rating)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                elif msg == '7': #################################################### Delete rating of a movie
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    result = movie_controller.delete_movie_rating(userId, movie_id)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                ######### Reviews

                elif msg == '8': #################################################### View all your reviews
                    result = movie_controller.list_reviews(userId)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                elif msg == '9': #################################################### View review of a movie
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    result = movie_controller.read_review(userId, movie_id)
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                elif msg == '10': #################################################### Create/Update review of a movie
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    client.send(sign_and_encrypt(box, server_signing_key, 'Review Title: '))
                    title = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    client.send(sign_and_encrypt(box, server_signing_key, 'Review Body: '))
                    review = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    result = movie_controller.create_update_review(userId, movie_id, title, review)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                elif msg == '11': #################################################### Delete review of a movie
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    result = movie_controller.delete_review(userId, movie_id)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break

                elif msg == 'quit': #################################################### Exit application
                    client.send(sign_and_encrypt(box, server_signing_key, "quit"))
                    client.close()
                    del clients[client]
                    print(clients)
                    quit = True
                    break
                else:
                    break
            else:
                break


#################################################### Establish Host & Port
clients = {}
addresses = {}
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#################################################### Check for private key file
if not os.path.isfile('server_private_key'):
    skserver = PrivateKey.generate()
    f = open("server_private_key", "wb")
    f.write(bytes(skserver))
    f.close()
file = open("server_private_key", "rb")
key = file.read()

skserver = PrivateKey(key)
pkserver = skserver.public_key
server_signing_key = nacl.signing.SigningKey(bytes(skserver))
server_verify_key = server_signing_key.verify_key

#################################################### Establish Modules
db = DB()
graphdb = neo4jDB()
movie_store = MovieStore(db, graphdb)
movie_view = MovieView()
movie_controller = MovieController(movie_store, movie_view)
user_store = UserStore(db, graphdb)
user_view = UserView()
user_controller = UserController(user_store, user_view)

#################################################### Run tests
for res in user_store.test():
    print(res)
print('neo4j', movie_store.test())
for res in movie_store.get_rated_movies(1):
    print(res)

#################################################### Listen for connections
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()