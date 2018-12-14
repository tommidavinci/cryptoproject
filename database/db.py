import psycopg2
from database.config import config


class DB:

    def __init__(self):
        self.conn = None

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            #print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            self.conn = conn
            return self.conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def query(self, sql):
        if not self.conn:
            self.conn = self.connect()
        cur = self.conn.cursor()
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
        return records