import time
import psycopg2
import discord


class WaifuManager:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.player_waifu = {}
        self.players = None
        self.waifus = None
        self.current_waifu_spawn = None
        self.prepared_waifu_spawn = None
        self.is_prepared = False

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.load_player_waifu()
    
    def add_waifu_to_player(self, mal_id, name, discord_id):
        mal_id = str(mal_id)
        discord_id = str(discord_id)
        if self.player_waifu.get(discord_id, None) is None:
            self.player_waifu[discord_id] = []
        self.waifus.add_waifu(mal_id, name)
        waifu_id = self.waifus.get_latest_waifu_id(mal_id)
        player_id = self.players.get_player_id(discord_id)
        self.player_waifu[discord_id].append(waifu_id)
        self.cur.execute("INSERT INTO player_waifu (player_id, waifu_id) VALUES (%s, %s)", (player_id, waifu_id))
        self.save()
    
    def load_player_waifu(self):
        self.cur.execute("SELECT player_id, waifu_id FROM player_waifu;")
        query = self.cur.fetchall()
        for row in query:
            player_id, waifu_id = row
            discord_id = self.players.get_player_by_id(player_id)
            if self.player_waifu.get(discord_id, None) is None:
                self.player_waifu[discord_id] = []
            self.player_waifu[discord_id].append(waifu_id)
    
    def prepare_waifu_spawn(self, waifu_props):
        mal_id = str(waifu_props['mal_id'])
        name = waifu_props['name']
        image_url = waifu_props['image_url']
        self.prepared_waifu_spawn = WaifuSpawn(mal_id, name, image_url)
        self.is_prepared = True
    
    def spawn_waifu(self):
        self.current_waifu_spawn = self.prepared_waifu_spawn
        self.prepared_waifu_spawn = None
        self.is_prepared = False
        return self.current_waifu_spawn.embed
    
    def waifu_claimed(self):
        self.current_waifu_spawn = None

    def save(self):
        self.conn.commit()


class WaifuSpawn:

    def __init__(self, mal_id, name, image_url):
        self.mal_id = mal_id
        self.name = name
        self.image_url = image_url
        self.embed = None
        self.prepare()

    def prepare(self):
        initials = self.get_initials()
        embed = discord.Embed(title="Waifu Spawn",
                                description="A wild waifu appeared.\n`?claim name` to catch them.\n\
                                Their initials are `{}`".format(initials),
                                color=0x07FAA2)
        embed._image = {
            'url': str(self.image_url)
        }
        self.embed = embed

    def get_initials(self):
        words = self.name.split(' ')
        print(words)
        initials = ""
        for word in words:
            initials += word[0]
            initials += '. '
        return initials


waifu_manager = WaifuManager()
