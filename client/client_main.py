import nacl.secret
import nacl.utils
import nacl.signing
import pickle
from socket import AF_INET, socket, SOCK_STREAM
from nacl.public import PrivateKey, Box, PublicKey
from nacl.signing import VerifyKey
from common_functions import sign_and_encrypt, decrypt_and_verify


HOST = input('Enter host: ')
if not HOST:
    HOST = "localhost"
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 4096
ADDR = (HOST, PORT)

skclient = PrivateKey.generate()
pkclient = skclient.public_key
client_signing_key = nacl.signing.SigningKey(bytes(skclient))
client_verify_key = client_signing_key.verify_key


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

combined_key = pickle.loads(client_socket.recv(BUFSIZ))
server_publickey = PublicKey(combined_key[0])
server_verify_key = VerifyKey(combined_key[1])
client_server_box = Box(skclient, server_publickey)

client_socket.send(pickle.dumps([bytes(pkclient), bytes(client_verify_key)]))

symmetric_privatekey_bytes = client_socket.recv(BUFSIZ)
symmetric_privatekey = client_server_box.decrypt(symmetric_privatekey_bytes)
symmetric_secret_key_box_client = nacl.secret.SecretBox(symmetric_privatekey)

msg_encrypted = client_socket.recv(BUFSIZ)
msg = decrypt_and_verify(symmetric_secret_key_box_client, server_verify_key, msg_encrypted)
print(msg)
name = input()
client_socket.send(sign_and_encrypt(symmetric_secret_key_box_client, client_signing_key, name))

while True:
    try:
        msg_encrypted = client_socket.recv(BUFSIZ)
        msg = decrypt_and_verify(symmetric_secret_key_box_client, server_verify_key, msg_encrypted)
        print(msg)
        if msg == "quit":
            print("closing...")
            client_socket.close()
            break
        selection = input()
        encrypted = sign_and_encrypt(symmetric_secret_key_box_client, client_signing_key, selection)
        client_socket.send(encrypted)


    except OSError:  # Possibly client has left the chat.
        break


