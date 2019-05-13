import datetime


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
        self.cur.execute("SELECT id, currency, won_fights, lost_fights, gist_id, new_gacha FROM players;")
        query = self.cur.fetchall()
        for row in query:
            _id, currency, won_fights, lost_fights, gist_id, new_gacha = row
            self.players[str(_id)] = Player(str(_id), int(won_fights),
                                            int(lost_fights), int(currency), gist_id, new_gacha)

    def add_player(self, _id, username):
        _id = str(_id)
        if _id in self.players:
            return
        self.players[_id] = Player(_id)
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

    def update_player_gist_id(self, discord_id, gist_id):
        discord_id = str(discord_id)
        if discord_id not in self.players:
            return
        self.cur.execute("UPDATE players SET gist_id=%s WHERE id=%s;", (gist_id, discord_id))
        self.save()
        self.players[discord_id].gist_id = gist_id
    
    def update_gacha_time(self, player):
        self.cur.execute("SELECT now FROM now();")
        query = self.cur.fetchone()
        current_time = query[0]
        if current_time.hour < 6:
            new_time = current_time.replace(hour=6, minute=0, second=0)
        else:
            new_time = current_time + datetime.timedelta(days=1)
            new_time = new_time.replace(hour=6, minute=0, second=0)
        self.cur.execute("UPDATE players SET new_gacha=%s WHERE id=%s;", (new_time, player._id))
        self.save()
        player.new_gacha_time = new_time

    def save(self):
        self.conn.commit()


class Player:

    def __init__(self, _id, won_fights=0, lost_fights=0, currency=0, gist_id=None, new_gacha_time=None):
        self._id = _id
        self.won_fights = won_fights
        self.lost_fights = lost_fights
        self.currency = currency
        self.gist_id = gist_id
        self.new_gacha_time = new_gacha_time
        self.waifu_list = None

    def set_waifu_list(self, waifu_list):
        self.waifu_list = waifu_list

    def get_waifu_list(self):
        return self.waifu_list


players = Players()
