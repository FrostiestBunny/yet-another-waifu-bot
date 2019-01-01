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

@bot.command(pass_context=True)
async def random_waifu(ctx):
    failed_attempts = 0
    while True:
        char_id = random.randint(1, 99999)
        response = await get_waifu_by_id(char_id)
        error = response.get('error', None)
        if error is None:
            waifu_manager.add_waifu_to_player(response['mal_id'], response['name'], ctx.message.author.id)
            print("Added waifu")
            if failed_attempts > 0:
                await bot.say("Failed attempts: {}".format(failed_attempts))
            return
        failed_attempts += 1
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
