import time
import psycopg2
import discord


class Players:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.players = {}

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.load_players()
    
    def load_players(self):
        self.cur.execute("SELECT id, currency, won_fights, lost_fights FROM players;")
        query = self.cur.fetchall()
        for row in query:
            _id, currency, won_fights, lost_fights = row
            self.players[str(_id)] = Player(str(_id), int(won_fights),
                                            int(lost_fights), int(currency))
    
    def add_player(self, _id, username):
        _id = str(_id)
        if _id in self.players:
            return
        self.players[_id] = Player(_id, username)
        self.cur.execute("INSERT INTO players (id, currency, won_fights, lost_fights)\
                          VALUES (%s, %s, %s, %s)", (_id, 0, 0, 0))
        self.save()
    
    def get_player_id(self, discord_id):
        self.cur.execute("SELECT player_id FROM players WHERE id=%s;", (discord_id,))
        query = self.cur.fetchone()
        player_id = query[0]
        return int(player_id)
    
    def get_player_by_id(self, player_id):
        self.cur.execute("SELECT id FROM players WHERE player_id=%s;", (player_id,))
        query = self.cur.fetchone()
        discord_id = query[0]
        return str(discord_id)

    def save(self):
        self.conn.commit()


class Player:

    def __init__(self, _id, won_fights=0, lost_fights=0, currency=0):
        self._id = _id
        self.won_fights = won_fights
        self.lost_fights = lost_fights
        self.currency = currency
        self.waifu_list = None
    
    def set_waifu_list(self, waifu_list):
        self.waifu_list = waifu_list
    
    def get_waifu_list(self):
        return self.waifu_list


players = Players()
