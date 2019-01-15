import discord
from bot import bot
import aiohttp
import asyncio
import random
from player import players
from waifu_manager import waifu_manager
from http_session import http_session
import json


API_URL = "https://api.jikan.moe/v3/"


async def find_mal(kind, name, limit):
    response = ""
    params = {'q': name, 'limit': limit}
    session = http_session.get_connection()
    async with session.get(API_URL + "search/{}/".format(kind), params=params) as resp:
        response = await resp.json()
    
    error = response.get('error', None)
    if error is not None:
        return None
    msg = ""
    return response


@bot.command(pass_context=True)
async def lookup(ctx, *args: str):
    name = ' '.join(args)
    message = ""
    response = await find_mal("character", name, 30)
    if response is None:
        await bot.say("Character not found")
        return
    for character in response['results']:
        character_name = character['name'].split(', ')
        character_name.reverse()
        character_name = ' '.join(character_name)
        if name.lower() not in character_name.lower():
            continue
        message += str(character['mal_id'])
        message += " | "
        message += character_name
        message += "\n"
    embed = discord.Embed(title="Lookup: {}".format(name), description=message, color=0x200FB4)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def info(ctx, *args: str):
    args = list(args)
    is_extended = False
    if args[-1].startswith('-extended'):
        DESCRIPTION_LIMIT = 1997
        SERIES_LIMIT = 20
        footer = "Use ?info to view shorter description."
        is_extended = True
        del args[-1]
    else:
        DESCRIPTION_LIMIT = 249
        SERIES_LIMIT = 2
        footer = "Use ?info name -extended to view extended description."
    if args[0].isdigit():
        response = await get_waifu_by_id(args[0])
        if response is None:
            await bot.say("No character with that id found")
            return
    else:
        name = ' '.join(args)
        character_id = None
        response = await find_mal("character", name, 1)
        if response is None:
            await bot.say("Character not found")
            return
        character = response['results'][0]
        character_id = str(character['mal_id'])
        response = ""
        session = http_session.get_connection()
        async with session.get(API_URL + "/character/{}/".format(character_id)) as resp:
            response = await resp.json()

    description = response['about'][:DESCRIPTION_LIMIT]
    if len(response['about']) > DESCRIPTION_LIMIT:
        description += '...'
    title = response['name'] + " ({}) ({})".format(response['name_kanji'], response['mal_id'])
    embed = discord.Embed(title=title, description=description, color=0x8700B6 )
    if response.get('animeography', None) is not None and response['animeography'] != []:
        anime_list = ""
        counter = 0
        for anime in response['animeography']:
            if counter == SERIES_LIMIT:
                anime_list += "..."
                break
            anime_list += anime['name']
            anime_list += "\n"
            counter += 1
        embed.add_field(name="Anime", value=anime_list, inline=False)
    if response.get('mangaography', None) is not None and response['mangaography'] != []:
        manga_list = ""
        counter = 0
        for manga in response['mangaography']:
            if counter == SERIES_LIMIT:
                manga_list += "..."
                break
            manga_list += manga['name']
            manga_list += "\n"
            counter += 1
        embed.add_field(name="Manga", value=manga_list, inline=False)
    if is_extended:
        embed.add_field(name="Favorites", value=response['member_favorites'])
    embed._image = {
            'url': str(response['image_url'])
        }
    embed.set_footer(text=footer)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def series_lookup(ctx, *args: str):
    message = ""
    name = ' '.join(args)
    anime_response = await find_mal("anime", name, 15)
    manga_response = await find_mal("manga", name, 15)
    if anime_response is None and manga_response is None:
        await bot.say("Series not found")
        return
    if anime_response is not None:
        for anime in anime_response['results']:
            if name.lower() not in anime['title'].lower():
                continue
            message += str(anime['mal_id'])
            message += " | "
            message += anime['title']
            message += " (A)"
            message += "\n"
    if manga_response is not None:
        for manga in manga_response['results']:
            if name.lower() not in manga['title'].lower():
                continue
            message += str(manga['mal_id'])
            message += " | "
            message += manga['title']
            message += " (M)"
            message += "\n"
    embed = discord.Embed(title="Lookup: {}".format(name), description=message, color=0x200FB4)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def series_info(ctx, *args: str):
    args = list(args)
    if args[-1].startswith('-m'):
        is_anime = False
        del args[-1]
    else:
        is_anime = True
    if args[0].isdigit():
        response = await get_series_characters_by_id("anime", args[0])
        if response is None or not is_anime:
            is_anime = False
            response = await get_series_characters_by_id("manga", args[0])
            if response is None:
                await bot.say("No series with this id")
                return
    else:
        name = ' '.join(args)
        series_id = None
        response = await find_mal("anime", name, 1)
        if response is None or not is_anime:
            is_anime = False
            response = await find_mal("manga", name, 1)
            if response is None:
                await bot.say("Series not found")
                return
        series = response['results'][0]
        series_id = str(series['mal_id'])
        session = http_session.get_connection()
        if is_anime:
            response = await get_series_characters_by_id("anime", series_id)
        else:
            response = await get_series_characters_by_id("manga", series_id)

    message = ""
    counter = 0
    if is_anime:
        footer = "If you wanted a manga with the same id, use the same command with -m at the end.\n"
    else:
        footer = ""
    for character in response['characters']:
        if counter == 30:
            footer += "{} characters omitted.".format(len(response['characters']) - counter)
            break
        message += str(character['mal_id'])
        message += " | "
        character_name = character['name'].split(', ')
        character_name.reverse()
        character_name = ' '.join(character_name)
        message += character_name
        message += "\n"
        counter += 1
    embed = discord.Embed(title=response['title'], description=message, color=0x200FB4)
    embed.set_footer(text=footer)
    await bot.send_message(ctx.message.channel, embed=embed)


async def random_waifu(channel):
    DEFAULT_IMAGE_URL = "https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png"
    if waifu_manager.current_waifu_spawn is not None:
        return
    if waifu_manager.is_prepared:
        response = waifu_manager.spawn_waifu()
        message = await bot.send_message(channel, embed=response)
        waifu_manager.set_claim_message(message)
    while True:
        char_id = random.randint(1, 99999)
        response = await get_waifu_by_id(char_id)
        if response is not None:
            if response['image_url'] != DEFAULT_IMAGE_URL and response['member_favorites'] >= 5:
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


async def get_series_characters_by_id(kind, mal_id):
    session = http_session.get_connection()
    if kind == "anime":
        async with session.get(API_URL + "{}/{}/characters_staff".format(kind, mal_id)) as resp:
            response = await resp.json()
        async with session.get(API_URL + "{}/{}".format(kind, mal_id)) as resp:
            anime = await resp.json()
        response['title'] = anime.get('title', "") + " (A)"
    else:
        async with session.get(API_URL + "{}/{}/characters".format(kind, mal_id)) as resp:
            response = await resp.json()
        async with session.get(API_URL + "{}/{}".format(kind, mal_id)) as resp:
            manga = await resp.json()
        response['title'] = manga.get('title', "") + " (M)"

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
        waifu_manager.waifu_claimed(ctx.message.author.id)
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
    embed = await waifu_manager.get_player_waifus(ctx.message.author.id, ctx.message.author.name, page)
    if embed is None:
        await bot.say("No waifus, that's pretty sad.")
        return
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


@bot.command(pass_context=True)
async def praise(ctx, member: discord.Member):
    author = ctx.message.author
    if member.id == author.id:
        await bot.say("Praising yourself? How sad.\n*pats*")
    elif member.id == bot.user.id:
        await bot.say("Thanks! You are pretty cool yourself.")
    else:
        await bot.say("{}, you have been praised by {}! How nice of them!".format(member.mention, author.name))
