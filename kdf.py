from nacl import pwhash, utils

#################################################### Setup
size = pwhash.argon2id.BYTES_MIN

#################################################### Hash by Key-Derivation
def hash_password(password, salt = utils.random(pwhash.argon2id.SALTBYTES)):
    hashed_password = pwhash.argon2id.kdf(size, bytes(password, 'utf-8'), salt)
    return (hashed_password, salt)

#################################################### Verify Password match
def verify_password(password, salt, hashed_password):
    return hash_password(password, salt)[0] == hashed_password