import argparse
import discord
from discord.ext import commands
from glob import glob
from player import players
from waifu import waifus
from waifu_manager import waifu_manager
from bot_config import bot_config
from GG import gg_manager
import os
import random
import github_api
from http_session import http_session

TOKEN = os.getenv('WAIFU_BOT_TOKEN')
APPROVED_SERVERS = ["MordredBot Dev", "Newt3012's Lets Play Discussion"]
LAST_STATUS = None
LAST_GAME = None

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--maintenance", help="turn on maintenance mode",
                    action="store_true")
COMMAND_ARGS = parser.parse_args()

description = """The best waifu bot."""
bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    global COMMAND_ARGS
    load_extensions()
    http_session.connect()
    bot_config.connect(gg_manager.conn)
    players.connect(gg_manager.conn)
    waifus.connect(gg_manager.conn)
    waifu_manager.players = players
    waifu_manager.waifus = waifus

    if COMMAND_ARGS.maintenance:
        await bot.change_presence(
            game=discord.Game(name="Dad's working on me"),
            status=discord.Status.dnd)
    else:
        waifu_manager.connect(gg_manager.conn)
    
    waifu_commands = bot.get_cog('WaifuCommands')
    await waifu_commands.random_waifu(None)
    await update_messages()
    print("Logged in")


def load_extensions():
    extensions = get_extensions()
    for ext in extensions:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(e)


def get_extensions():
    ext = glob('cogs/[!_]*.py')
    return [i.replace('\\', '.').replace('/', '.')[:-3] for i in ext]


async def update_messages():
    channel = await get_suggestion_channel()
    async for message in bot.logs_from(channel):
        bot.messages.append(message)


async def get_suggestion_channel():
    for server in bot.servers:
        if server.name == "MordredBot Dev":
            for channel in server.channels:
                if channel.name == "suggestions":
                    return channel


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return

    if bot.user in message.mentions:
        if message.content.lower().endswith("alright?") and\
                message.author.id == "178887072864665600":
            await bot.send_message(message.channel, "Sure, dad.")
        return

    if message.content == '\o':
        await bot.send_message(message.channel, 'o/')
    elif message.content == 'o/':
        await bot.send_message(message.channel, '\o')
    if message.server.name in APPROVED_SERVERS:
        if random.randint(0, 99) < 1:
            channel = bot.get_channel(bot_config.spawn_channel_id)
            if channel is not None:
                waifu_commands = bot.get_cog('WaifuCommands')
                await waifu_commands.random_waifu(channel)


@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if is_suggestion(message, user):
        if reaction.emoji.name == "no_emoji":
            await bot.delete_message(message)
        elif reaction.emoji.name == "yes_emoji":
            await github_api.create_card(message.embeds[0]['description'])
            await bot.delete_message(message)


def is_suggestion(message, user):
    return message.server.name == "MordredBot Dev"\
        and message.channel.name == "suggestions"\
        and user.id == '178887072864665600'


@bot.command(pass_context=True)
async def suggest(ctx, *args):
    suggestion = ' '.join(args)
    description = suggestion
    embed = discord.Embed(title=ctx.message.author.name, description=description,
                          color=0x0760FA)
    channel = await get_suggestion_channel()
    message = await bot.send_message(channel, embed=embed)
    await bot.add_reaction(message, ':yes_emoji:529842623532367872')
    await bot.add_reaction(message, ':no_emoji:529843815415021587')
    await bot.add_reaction(ctx.message, '👌')


@bot.command(pass_context=True)
async def get_commits(ctx):
    response = await github_api.get_commits()
    message = ""
    response = response[:10]
    for row in response:
        commit_author = row['commit']['author']['name']
        commit_message = row['commit']['message']
        message += "**" + commit_author + "**"
        message += ":\n"
        message += commit_message
        message += "\n\n"

    embed = discord.Embed(title="Commits:", description=message, color=0x27F0DE)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def set_spawn_channel(ctx, channel: discord.Channel):
    bot_config.update_config(channel.id)
    await bot.say("Spawn channel set to {}".format(channel.mention))


@bot.command(pass_context=True)
async def set_game(ctx, *args: str):
    global LAST_STATUS
    global LAST_GAME
    if ctx.message.author.id != "178887072864665600":
        await bot.say("You're not my dad.")
        return
    name = ' '.join(args)
    game = discord.Game(name=name)
    LAST_GAME = game
    await bot.change_presence(game=game, status=LAST_STATUS)


@bot.command(pass_context=True)
async def set_status(ctx, status):
    global LAST_STATUS
    global LAST_GAME
    if ctx.message.author.id != "178887072864665600":
        await bot.say("You're not my dad.")
        return
    states = {
        'online': discord.Status.online,
        'offline': discord.Status.offline,
        'idle': discord.Status.idle,
        'dnd': discord.Status.dnd
    }
    status = states[status]
    LAST_STATUS = status
    await bot.change_presence(status=status, game=LAST_GAME)


bot.run(TOKEN)
