import discord
from bot import bot
from GG import gg_manager
import currency
import games
import image_fun
from person import people
from player import players
from waifu import waifus
from waifu_manager import waifu_manager
from bot_config import bot_config
import waifu_commands
import os
import random
import github_api
from http_session import http_session

TOKEN = os.getenv('WAIFU_BOT_TOKEN')
APPROVED_SERVERS = ["MordredBot Dev", "Newt3012's Lets Play Discussion"]


@bot.event
async def on_ready():
    http_session.connect()
    bot_config.connect(gg_manager.conn)
    people.connect(gg_manager.conn)
    players.connect(gg_manager.conn)
    waifus.connect(gg_manager.conn)
    waifu_manager.players = players
    waifu_manager.waifus = waifus
    waifu_manager.connect(gg_manager.conn)
    await waifu_commands.random_waifu(None)
    await update_messages()
    print("Logged in")


async def update_messages():
    channel = await waifu_commands.get_suggestion_channel()
    async for message in bot.logs_from(channel):
        bot.messages.append(message)


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return

    if message.content == '\o':
        await bot.send_message(message.channel, 'o/')
    elif message.content == 'o/':
        await bot.send_message(message.channel, '\o')
    if message.server.name in APPROVED_SERVERS:
        if random.randint(0, 99) < 3:
            channel = bot.get_channel(bot_config.spawn_channel_id)
            if channel is not None:
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
async def get_commits(ctx):
    response = await github_api.get_commits()
    message = ""
    counter = 0
    for row in response:
        if counter == 5:
            break
        commit_author = row['commit']['author']['name']
        commit_message = row['commit']['message']
        message += "**" + commit_author + "**"
        message += ":\n"
        message += commit_message
        message += "\n\n"
        counter += 1
    
    embed = discord.Embed(title="Commits:", description=message, color=0x27F0DE)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def set_spawn_channel(ctx, channel: discord.Channel):
    bot_config.update_config(channel.id)
    await bot.say("Spawn channel set to {}".format(channel.mention))


bot.run(TOKEN)
