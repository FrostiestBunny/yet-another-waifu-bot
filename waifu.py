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
        print("Loading waifus")
        self.cur.execute("SELECT waifu_id, name, nickname, affection, stats,\
                          mal_id, last_interaction, acquired, is_comicvine FROM waifus;")
        query = self.cur.fetchall()
        for row in query:
            waifu_id, name, nickname, affection, stats, mal_id, last_interaction, acquired, is_comicvine = row
            self.waifus[int(waifu_id)] = Waifu(int(waifu_id), str(mal_id), str(name), is_comicvine,
                                               str(nickname), int(affection), str(stats),
                                               str(last_interaction), str(acquired))
        print("waifus loaded")

    def add_waifu(self, mal_id, name, is_comicvine):
        mal_id = str(mal_id)
        self.cur.execute("INSERT INTO waifus (name, nickname, affection, stats,\
                        mal_id, last_interaction, acquired, is_comicvine)\
                        VALUES (%s, %s, %s, %s, %s, %s, now()::timestamp, %s)",
                         (name, None, 0, "1:1:1", mal_id, None, is_comicvine))
        self.save()
        waifu_id = self.get_latest_waifu_id(mal_id)
        self.waifus[waifu_id] = Waifu(waifu_id, mal_id, name, is_comicvine)

    def get_latest_waifu_id(self, mal_id):
        self.cur.execute(
            "SELECT waifu_id FROM waifus WHERE mal_id=%s ORDER BY acquired DESC LIMIT 1;",
            (mal_id,))
        query = self.cur.fetchone()
        waifu_id = query[0]
        return int(waifu_id)

    def save(self):
        self.conn.commit()


class Waifu:

    def __init__(self, waifu_id, mal_id, name, is_comicvine, nickname=None,
                 affection=0, stats="1:1:1", last_interaction=None, acquired=None):
        self.waifu_id = waifu_id
        self.mal_id = mal_id
        self.name = name
        self.is_comicvine = is_comicvine
        self.nickname = nickname
        self.affection = affection
        self.stats = stats
        self.last_interaction = last_interaction
        self.acquired = acquired


waifus = Waifus()
