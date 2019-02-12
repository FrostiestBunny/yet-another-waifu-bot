import time
import psycopg2
import discord
import asyncio
import random
import math


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
        self.claim_message = None

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.load_player_waifu()
    
    def set_claim_message(self, claim_message):
        self.claim_message = claim_message
    
    def add_waifu_to_player(self, mal_id, name, discord_id):
        mal_id = str(mal_id)
        discord_id = str(discord_id)
        if self.player_waifu.get(discord_id, None) is None:
            self.player_waifu[discord_id] = []
        self.waifus.add_waifu(mal_id, name)
        waifu_id = self.waifus.get_latest_waifu_id(mal_id)
        player_id = self.players.get_player_id(discord_id)
        self.player_waifu[discord_id].append(waifu_id)
        player = self.players.players[discord_id]
        if player.get_waifu_list() is not None:
            player.get_waifu_list().append(self.waifus.waifus[waifu_id])
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
            self.player_waifu[discord_id].append(int(waifu_id))
    
    def prepare_waifu_spawn(self, waifu_props, pictures):
        mal_id = str(waifu_props['mal_id'])
        name = waifu_props['name']
        try:
            image_url = random.choice(pictures)['large']
        except IndexError:
            image_url = waifu_props['image_url']
        self.prepared_waifu_spawn = WaifuSpawn(mal_id, name, image_url)
        self.is_prepared = True
    
    def spawn_waifu(self):
        self.current_waifu_spawn = self.prepared_waifu_spawn
        self.prepared_waifu_spawn = None
        self.is_prepared = False
        return self.current_waifu_spawn.embed
    
    def waifu_claimed(self, discord_id):
        mal_id = self.current_waifu_spawn.mal_id
        name = self.current_waifu_spawn.name
        self.current_waifu_spawn = None
        self.add_waifu_to_player(mal_id, name, discord_id)
    
    async def skip_waifu(self):
        self.current_waifu_spawn = None
    
    async def get_player_waifus(self, discord_id, name, page):
        waifus = []
        if self.player_waifu.get(discord_id, None) is None:
            return None
        
        player = self.players.players[discord_id]

        if player.get_waifu_list() is None:
            for waifu_id in self.player_waifu[discord_id]:
                waifus.append(self.waifus.waifus[waifu_id])
            player.set_waifu_list(waifus)
        waifus = player.get_waifu_list()
        message = ""
        offset = 20
        start = offset * (page - 1)
        max_pages = math.ceil(len(waifus) / offset)
        if start >= len(waifus):
            return
        end = offset * page
        for n, waifu in enumerate(waifus[start:end], start):
            message += str(n)
            message += " | "
            message += waifu.name
            message += " | Affection: {}".format(waifu.affection)
            message += "\n"
        title = "{}'s waifus (page {}):".format(name, page)
        footer = "Page {} of {}".format(page, max_pages)
        embed = discord.Embed(title=title, description=message, color=0xB346D8)
        embed.set_footer(text=footer)
        return embed

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
        initials = ""
        for word in words:
            if word == '':
                continue
            initials += word[0]
            initials += '. '
        return initials


waifu_manager = WaifuManager()
