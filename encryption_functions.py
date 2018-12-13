import nacl.encoding
import nacl.signing
import nacl.secret
import nacl.utils
from nacl.public import PrivateKey, Box, PublicKey

def signed_encrypted(symmetric_box, signing_key, plain_text):
    signed = signing_key.sign(bytes(plain_text, "utf8"))
    encrypted_text = symmetric_box.encrypt(signed)
    return encrypted_text

def decrypted_verify(symmetric_box, verify_key, encrypted_text):
    signed = symmetric_box.decrypt(encrypted_text)
    plain_text = verify_key.verify(signed).decode('utf8')
    return plain_text
