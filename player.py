import time
import psycopg2


class Players:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.players = {}

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def save(self):
        self.conn.commit()


players = Players()
