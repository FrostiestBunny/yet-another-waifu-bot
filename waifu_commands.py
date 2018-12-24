import discord
from bot import bot
import aiohttp
import asyncio
import random

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
        response = ""
        char_id = random.randint(1, 99999)
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL + "character/{}".format(char_id)) as resp:
                response = await resp.json()
        
        error = response.get('error', None)
        if error is None:
            await bot.say(response['url'])
            if failed_attempts > 0:
                await bot.say("Failed attempts: {}".format(failed_attempts))
            return
        failed_attempts += 1
        await asyncio.sleep(3)
