from nacl import pwhash, utils

size = pwhash.argon2i.BYTES_MIN

def hash_password(password, salt = utils.random(pwhash.argon2i.SALTBYTES)):
    hashed_password = pwhash.argon2i.kdf(size, bytes(password, 'utf-8'), salt)
    return (hashed_password, salt)

def verify_password(password, salt, hashed_password):
    return hash_password(password, salt)[0] == hashed_password
    #pwhash.argon2i.verify(hash_password, bytes(password, 'utf-8'))

#h_s = hash_password('bla')
#print(h_s)
#print (verify_password('bla', h_s[1], h_s[0]))