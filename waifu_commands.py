import discord
from bot import bot
import aiohttp
import asyncio
import random
from player import players
from waifu_manager import waifu_manager
from http_session import http_session


API_URL = "https://api.jikan.moe/v3/"


async def find_waifu(name, limit):
    response = ""
    params = {'q': name, 'limit': limit}
    session = http_session.get_connection()
    async with session.get(API_URL + "search/character/", params=params) as resp:
        response = await resp.json()
    
    error = response.get('error', None)
    if error is not None:
        await bot.say("Character not found.")
        return
    msg = ""
    return response


@bot.command(pass_context=True)
async def lookup(ctx, *args: str):
    name = ' '.join(args)
    message = ""
    response = await find_waifu(name, 20)
    for character in response['results']:
        character_name = character['name'].split(', ')
        character_name.reverse()
        character_name = ' '.join(character_name)
        if name.lower() not in character_name.lower():
            continue
        message += str(character['mal_id'])
        message += ": "
        message += character_name
        message += "\n"
    embed = discord.Embed(title="Lookup: {}".format(name), description=message, color=0x200FB4)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def info(ctx, *args: str):
    if args[0].isdigit():
        response = await get_waifu_by_id(args[0])
        if response is None:
            await bot.say("No character with that id found")
            return
    else:
        name = ' '.join(args)
        character_id = None
        response = await find_waifu(name, 1)
        character = response['results'][0]
        character_id = str(character['mal_id'])
        response = ""
        session = http_session.get_connection()
        async with session.get(API_URL + "/character/{}/".format(character_id)) as resp:
            response = await resp.json()

    description = response['about'][:249]
    description += '...'
    title = response['name'] + " ({}) ({})".format(response['name_kanji'], response['mal_id'])
    embed = discord.Embed(title=title, description=description, color=0x8700B6 )
    if response.get('animeography', None) is not None and response['animeography'] != []:
        anime_list = ""
        counter = 0
        for anime in response['animeography']:
            if counter == 2:
                anime_list += "..."
                break
            anime_list += anime['name']
            anime_list += "\n"
            counter += 1
        embed.add_field(name="Anime", value=anime_list, inline=False)
    embed._image = {
            'url': str(response['image_url'])
        }
    embed.set_footer(text="Extended info soon")
    await bot.send_message(ctx.message.channel, embed=embed)


async def random_waifu(channel):
    if waifu_manager.current_waifu_spawn is not None:
        return
    if waifu_manager.is_prepared:
        response = waifu_manager.spawn_waifu()
        message = await bot.send_message(channel, embed=response)
        waifu_manager.set_claim_message(message)
    while True:
        char_id = random.randint(1, 99999)
        response = await get_waifu_by_id(char_id)
        error = response.get('error', None)
        if error is None:
            waifu_manager.prepare_waifu_spawn(response)
            return
        await asyncio.sleep(3)


async def get_waifu_by_id(mal_id):
    session = http_session.get_connection()
    async with session.get(API_URL + "character/{}".format(mal_id)) as resp:
        response = await resp.json()
    error = response.get('error', None)
    if error is not None:
        return None
    return response


@bot.command(pass_context=True)
async def spawn(ctx):
    await random_waifu(ctx.message.channel)


@bot.command(pass_context=True)
async def add_players(ctx):
    server = ctx.message.server
    for member in server.members:
        if not member.bot:
            players.add_player(member.id, member.name)
    await bot.say("Updated player database")


@bot.command(pass_context=True)
async def claim(ctx, *args: str):
    if waifu_manager.current_waifu_spawn is None:
        await bot.say("No active waifu spawn, what a shame.")
        return
    name = ' '.join(args)
    if name.lower() == waifu_manager.current_waifu_spawn.name.lower():
        await bot.say("You got it, {}! (But not really yet.)".format(ctx.message.author.mention))
        await waifu_manager.waifu_claimed(ctx.message.author.id)
        claim_message = waifu_manager.claim_message
        old_embed = claim_message.embeds[0]
        description = old_embed['description'] + "\n**Claimed by {}**".format(ctx.message.author.name)
        embed = discord.Embed(title=old_embed['title'], description=description, color=old_embed['color'])
        embed._image = {
            'url': old_embed['image']['url']
        }
        await bot.edit_message(claim_message, embed=embed)
    else:
        await bot.add_reaction(ctx.message, '❌')


@bot.command(pass_context=True)
async def skip(ctx):
    if waifu_manager.current_waifu_spawn is None:
        await bot.say("There's nothing to skip though 🤔")
        return
    await waifu_manager.skip_waifu()
    claim_message = waifu_manager.claim_message
    old_embed = claim_message.embeds[0]
    embed = discord.Embed(title=old_embed['title'], description="SKIPPED", color=old_embed['color'])
    await bot.edit_message(claim_message, embed=embed)


@bot.command(pass_context=True)
async def give_name_pls(ctx):
    await bot.say(
        "Name: {}.\n CHEATER ALERT (temp command obviously)".format(waifu_manager.current_waifu_spawn.name))


@bot.command(pass_context=True, name='list')
async def waifu_list(ctx, page: int=1):
    waifus = await waifu_manager.get_player_waifus(ctx.message.author.id)
    if waifus is None:
        await bot.say("No waifus, that's pretty sad.")
        return
    message = ""
    offset = 17
    start = offset * (page - 1)
    if start >= len(waifus):
        return
    end = offset * page
    for waifu in waifus[start:end]:
        message += waifu.name
        message += " | Affection: {}".format(waifu.affection)
        message += "\n"
    title = "{}'s waifus (page {}):".format(ctx.message.author.name, page)
    embed = discord.Embed(title=title, description=message, color=0xB346D8)
    await bot.send_message(ctx.message.channel, embed=embed)


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
