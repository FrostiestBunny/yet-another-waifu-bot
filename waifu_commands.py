import discord
from bot import bot
import aiohttp

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
