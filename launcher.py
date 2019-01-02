from bot import bot
from GG import gg_manager
import currency
import games
import image_fun
from person import people
from player import players
from waifu import waifus
from waifu_manager import waifu_manager
import waifu_commands
import os
import random

TOKEN = os.getenv('WAIFU_BOT_TOKEN')
APPROVED_SERVERS = ["MordredBot Dev", "Newt3012's Lets Play Discussion"]


@bot.event
async def on_ready():
    people.connect(gg_manager.conn)
    players.connect(gg_manager.conn)
    waifus.connect(gg_manager.conn)
    waifu_manager.players = players
    waifu_manager.waifus = waifus
    waifu_manager.connect(gg_manager.conn)
    await waifu_commands.random_waifu(None)
    print("Logged in")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return

    if message.content == '\o':
        await bot.send_message(message.channel, 'o/')
    elif message.content == 'o/':
        await bot.send_message(message.channel, '\o')
    if random.randint(0, 99) < 5:
        gg_manager.add(message.author.id, 10)
    if message.server.name in APPROVED_SERVERS and message.author.id == '178887072864665600':
        if random.randint(0, 99) < 25:
            await waifu_commands.random_waifu(message.channel)


bot.run(TOKEN)
