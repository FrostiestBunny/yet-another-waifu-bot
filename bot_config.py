import time
import psycopg2
import discord
import asyncio


class BotConfig:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.spawn_channel_id = None

    def connect(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()
        self.load_config()
    
    def load_config(self):
        self.cur.execute("SELECT spawn_channel FROM bot_config;")
        query = self.cur.fetchone()
        if query is None:
            return
        spawn_channel_id = query[0]
        self.spawn_channel_id = spawn_channel_id
    
    def update_config(self, spawn_channel_id):
        if self.spawn_channel_id is not None:
            self.alter_config(spawn_channel_id)
            return
        self.spawn_channel_id = spawn_channel_id
        self.cur.execute("INSERT INTO bot_config (spawn_channel) VALUES (%s)", (self.spawn_channel_id,))
        self.save()

    def alter_config(self, spawn_channel_id):
        self.cur.execute("UPDATE bot_config SET spawn_channel = %s WHERE spawn_channel=%s",
         (spawn_channel_id, self.spawn_channel_id,))
        self.save()
        self.spawn_channel_id = spawn_channel_id

    def save(self):
        self.conn.commit()


bot_config = BotConfig()
