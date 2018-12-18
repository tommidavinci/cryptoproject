from nacl import pwhash, utils

#################################################### Setup
size = pwhash.argon2i.BYTES_MIN

#################################################### Hash by Key-Derivation
def hash_password(password, salt = utils.random(pwhash.argon2i.SALTBYTES)):
    hashed_password = pwhash.argon2i.kdf(size, bytes(password, 'utf-8'), salt)
    return (hashed_password, salt)

#################################################### Verify Password match
def verify_password(password, salt, hashed_password):
    return hash_password(password, salt)[0] == hashed_password