import nacl.secret
import nacl.utils
import nacl.signing
import pickle
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


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
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

        ##encrypted = sign_and_encrypt(symmetric_secret_key_box_server, server_signing_key, "Greetings from the cave! Now type your name and press enter!")
        ##client.send(encrypted)

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_verify_key, symmetric_secret_key_box_server)).start()


def handle_client(client, client_verify_key, box):  # Takes client socket as argument.
    """Handles a single client connection."""
    quit = False
    userId = 0
    userName = "Anon"
    ##name_encrypted = client.recv(BUFSIZ)
    ##name = decrypt_and_verify(symmetric_secret_key_box_server, client_verify_key, name_encrypted)

  ## User Functionality
    #while quit == False:
    while quit == False:
        client.send(sign_and_encrypt(box, server_signing_key, '1. Login\n2. Signup:\n3. Anon'))
        msg = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))

        if msg == '3':
            quit = True
        else:
            client.send(sign_and_encrypt(box, server_signing_key, 'Username: '))
            username = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
            client.send(sign_and_encrypt(box, server_signing_key, 'Password: '))
            password = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))

            if msg == '1':
                #client.send(sign_and_encrypt(box, server_signing_key, '...Logging in...'))
                result = user_controller.login(username, password)
                if result is not None:
                    userId = result
                    userName = username
                    quit = True
                else:
                    client.send
                    
            elif msg == '2':
                #client.send(sign_and_encrypt(box, server_signing_key, '...Signing up...'))
                result = user_controller.signup(username, password)
                if result is not None:
                    userId = result
                    userName = username
                    quit = True
            #else:
            # else;
                ## username exists already? or just failed
           


    ## Server functionality    
    ##clients[client] = name
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
            if msg == '1':
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
            elif msg == '2':
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
            ## User only functions
            if userId > 0:
                if msg == '3':
                    result = movie_controller.get_rated_movies(userId)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break
                elif msg == '4':
                    result = movie_controller.get_precise_interested_movies(1)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                    break
                elif msg == '5':
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    client.send(sign_and_encrypt(box, server_signing_key, 'Rating: '))
                    rating = float(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    result = movie_controller.set_movie_rating(userId, movie_id, rating)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                elif msg == '6':
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    client.send(sign_and_encrypt(box, server_signing_key, 'Rating: '))
                    rating = float(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    result = movie_controller.set_movie_rating(userId, movie_id, rating)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                elif msg == '7':
                    client.send(sign_and_encrypt(box, server_signing_key, 'Movie ID: '))
                    movie_id = int(decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ)))
                    result = movie_controller.delete_movie_rating(userId, movie_id)
                    result += '\nSend any key to return to Home'
                    client.send(sign_and_encrypt(box, server_signing_key, result))
                    back = decrypt_and_verify(box, client_verify_key, client.recv(BUFSIZ))
                elif msg == 'quit':
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

server_signing_key = nacl.signing.SigningKey(bytes(skserver))
server_verify_key = server_signing_key.verify_key

db = DB()
graphdb = neo4jDB()
movie_store = MovieStore(db, graphdb)
movie_view = MovieView()
movie_controller = MovieController(movie_store, movie_view)
user_store = UserStore(db)
user_view = UserView()
user_controller = UserController(user_store, user_view)

for res in user_store.test():
    print(res)

print('neo4j', movie_store.test())

for res in movie_store.get_rated_movies(1):
    print(res)


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()