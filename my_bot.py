import discord
from discord.ext.commands import Bot
from glob import glob
import argparse
from player import players
from waifu import waifus
from waifu_manager import waifu_manager
from bot_config import bot_config
from GG import gg_manager
from http_session import http_session
import github_api
import random


APPROVED_SERVERS = ["MordredBot Dev", "Newt3012's Lets Play Discussion"]
LAST_STATUS = None
LAST_GAME = None

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--maintenance", help="turn on maintenance mode",
                    action="store_true")
COMMAND_ARGS = parser.parse_args()


class MyBot(Bot):

    async def on_ready(self):
        global COMMAND_ARGS
        self.load_my_extensions()
        http_session.connect()
        gg_manager.connect(COMMAND_ARGS.maintenance)
        bot_config.connect(gg_manager.conn)
        players.connect(gg_manager.conn)
        waifus.connect(gg_manager.conn)
        waifu_manager.players = players
        waifu_manager.waifus = waifus

        if COMMAND_ARGS.maintenance:
            game = discord.Game("undergoing surgery.")
            await self.change_presence(status=discord.Status.dnd, activity=game)

        waifu_manager.connect(gg_manager.conn)
        waifu_commands = self.get_cog('Waifu Commands')
        await waifu_commands.random_waifu(None)
        print("Logged in")
    
    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)

        if message.content == "\o":
            await message.channel.send("o/")
        elif message.content == "o/":
            await message.channel.send("\o")
        if message.guild.name in APPROVED_SERVERS:
            if random.randint(0, 99) < 1:
                channel = self.get_channel(int(bot_config.spawn_channel_id))
                if channel is not None:
                    waifu_commands = self.get_cog('Waifu Commands')
                    await waifu_commands.random_waifu(channel)
        
    def load_my_extensions(self):
        extensions = self.get_my_extensions()
        for ext in extensions:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(e)

    def get_my_extensions(self):
        ext = glob('cogs/[!_]*.py')
        return [i.replace('\\', '.').replace('/', '.')[:-3] for i in ext]

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        if channel.id != 529834032004071424:
            return
        message = await channel.get_message(payload.message_id)
        user = self.get_user(payload.user_id)
        emoji = payload.emoji
        if self.is_suggestion(message, user):
            if emoji.name == "no_emoji":
                await message.delete()
            elif emoji.name == "yes_emoji":
                await github_api.create_card(message.embeds[0].description)
                await message.delete()

    def is_suggestion(self, message, user):
        return message.guild.name == "MordredBot Dev"\
            and message.channel.name == "suggestions"\
            and user.id == 178887072864665600
    
    async def get_suggestion_channel(self):
        for guild in self.guilds:
            if guild.name == "MordredBot Dev":
                for channel in guild.channels:
                    if channel.name == "suggestions":
                        return channel
