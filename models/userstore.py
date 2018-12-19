from kdf import hash_password, verify_password

class UserStore:

    #################################################### Setup
    def __init__(self, db, graphdb):
        self.db = db
        self.graphdb = graphdb

    #################################################### Functionality
    def login(self, username, password):
        salt = bytes(self.db.query_with_params("select * from get_salt(%s)",[username])[0][0])
        h_s = hash_password(password, salt)
        result = self.db.query_with_params("select * from user_login_hashed_password(%s,%s)",
                                                [username, h_s[0]])
        if len(result) > 0:
            return result[0][0] # returns userId
        return None
        
    def signup(self, username, password):
        exists = self.db.query_with_params("select * from user_exists(%s)", [username])
        if exists[0] == True:
            return None
        else:
            h_s = hash_password(password)
            res = self.db.query_with_params("select * from insert_user(%s,%s,%s)",
                                                [username,h_s[0], h_s[1]])
            #if res is not None and res[0] > 0:
            if len(res) > 0:
                self.graphdb.create_user(res[0][0])
                return res[0][0] # the 1 row with userId, username

            return None

    #################################################### test
    def test(self):
        return self.db.query("select * from movies where movieId = 1")