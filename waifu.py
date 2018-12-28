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
        self.load_waifus()
    
    def load_waifus(self):
        self.cur.execute("SELECT name, nickname, affection, stats,\
                          mal_id, last_interaction, acquired FROM waifus;")
        query = self.cur.fetchall()
        for row in query:
            name, nickname, affection, stats, mal_id, last_interaction, acquired = row
            self.waifus[str(mal_id)] = Waifu(str(mal_id), str(name), str(nickname),
                                        int(affection), str(stats), str(last_interaction), str(acquired))
    
    def add_waifu(self, mal_id):
        self.waifus[mal_id] = Waifu(mal_id, username)
        self.cur.execute("INSERT INTO players (id, currency, won_fights, lost_fights)\
                          VALUES (%s, %s, %s, %s)", (_id, 0, 0, 0))
        self.save()

    def save(self):
        self.conn.commit()


class Waifu:

    def __init__(self, mal_id, name, nickname=None,
                 affection=0, stats="0:0:0", last_interaction=None, acquired=None):
        self.mal_id = mal_id
        self.name = name
        self.nickname = nickname
        self.affection = affection
        self.stats = stats
        self.last_interaction = last_interaction
        self.acquired = acquired


waifus = Waifus()
