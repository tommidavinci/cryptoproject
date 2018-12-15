from kdf import hash_password, verify_password

class UserStore:
    def __init__(self, db):
        self.db = db

    def test(self):
        return self.db.query("select * from movies where movieId = 1")

    def login(self, username, password):
        return 0
    
    def signup(self, username, password):
        h_s = (b'password', b'salt') ##hash_password(password)
        #val = '{0:b}'.format(h_s[0])
        #return 0
        res = self.db.query_with_params("select * from insert_user(%s,%s,%s)",(username, h_s[0], h_s[1]))
        #res = self.db.query("select * from insert_user({0!s},{1!s},{2!s})".format(username, h_s[0], h_s[1]))
        ##res = self.db.query('select * from insert_user('+ username +','+ h_s[0]+','+ h_s[1] +')')
        return res