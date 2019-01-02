import discord
from bot import bot
import aiohttp
import asyncio
import random
from player import players
from waifu_manager import waifu_manager


API_URL = "https://api.jikan.moe/v3/"


@bot.command(pass_context=True)
async def find_waifu(ctx, *args: str):
    name = ' '.join(args)
    response = ""
    params = {'q': name, 'limit': 3}
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL + "search/character/", params=params) as resp:
            response = await resp.json()
    
    error = response.get('error', None)
    if error is not None:
        await bot.say("Character not found.")
        return
    msg = ""
    for character in response['results']:
        msg += character['url']
        msg += '\n'
    await bot.say(msg)


async def random_waifu(channel):
    if waifu_manager.current_waifu_spawn is not None:
        return
    if waifu_manager.is_prepared:
        response = waifu_manager.spawn_waifu()
        await bot.send_message(channel, embed=response)
    while True:
        char_id = random.randint(1, 99999)
        response = await get_waifu_by_id(char_id)
        error = response.get('error', None)
        if error is None:
            waifu_manager.prepare_waifu_spawn(response)
            return
        await asyncio.sleep(3)


async def get_waifu_by_id(mal_id):
    async with aiohttp.ClientSession() as session:
            async with session.get(API_URL + "character/{}".format(mal_id)) as resp:
                response = await resp.json()
    return response


@bot.command(pass_context=True)
async def add_players(ctx):
    server = ctx.message.server
    for member in server.members:
        if not member.bot:
            players.add_player(member.id, member.name)
    await bot.say("Updated player database")


@bot.command(pass_context=True)
async def claim(ctx, *args: str):
    name = ' '.join(args)
    if name.lower() == waifu_manager.current_waifu_spawn.name.lower():
        await bot.say("You got it, {}! (But not really yet.)".format(ctx.message.author.mention))
        waifu_manager.waifu_claimed()
    else:
        await bot.say("Too bad, you suck.")


@bot.command(pass_context=True)
async def give_name_pls(ctx):
    await bot.say(
        "Name: {}.\n CHEATER ALERT (temp command obviously)".format(waifu_manager.current_waifu_spawn.name))


@bot.command(pass_context=True)
async def suggest(ctx, *args):
    suggestion = ' '.join(args)
    description = suggestion
    embed = discord.Embed(title=ctx.message.author.name, description=description, color=0x0760FA )
    channel = await get_suggestion_channel()
    message = await bot.send_message(channel, embed=embed)
    await bot.add_reaction(message, ':yes_emoji:529842623532367872')
    await bot.add_reaction(message, ':no_emoji:529843815415021587')
    await bot.add_reaction(ctx.message, '👌')


async def get_suggestion_channel():
    for server in bot.servers:
        if server.name == "MordredBot Dev":
            for channel in server.channels:
                if channel.name == "suggestions":
                    return channel
