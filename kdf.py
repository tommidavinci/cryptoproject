from nacl import pwhash, utils

#################################################### Setup
size = pwhash.argon2id.BYTES_MIN

#################################################### Hash by Key-Derivation
def hash_password(password, salt = utils.random(pwhash.argon2id.SALTBYTES)):
    hashed = pwhash.argon2id.kdf(size, bytes(password, 'utf-8'), salt)
    return (hashed, salt)

#################################################### Verify Password match
def verify_password(password, salt, hashed_password):
    return hash_password(password, salt)[0] == hashed_password

# p = b'password'
# h = b'("\205#k|\342_\327Df\322\211\256\342\024'

# print(pwhash.argon2i.verify(h,p))