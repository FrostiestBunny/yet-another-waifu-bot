import time
import psycopg2


class Waifus:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.waifus = {}

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def save(self):
        self.conn.commit()


waifus = Waifus()
