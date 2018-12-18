from database.db import DB
from kdf import hash_password

#################################################### Creates users 1-9 with username: UserX, and password: passwordx,
####################################################    where X is their number (1-9).
db = DB()
for i in range(1,10):
    h_s = hash_password('password'+str(i))
    db.execute("update users set password = %s, salt = %s where userId = %s;",
    [h_s[0], h_s[1], i])
    print('User'+str(i)+': password'+str(i)+' created')