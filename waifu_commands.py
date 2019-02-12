import discord
from bot import bot
import aiohttp
import asyncio
import random
from player import players
from waifu_manager import waifu_manager
from http_session import http_session
import json
import itertools
from difflib import SequenceMatcher
from timers import timers
import os


WAIFU_CLAIM_DELTA = 60
API_URL = "https://api.jikan.moe/v3/"
COMICVINE_API_KEY = os.getenv("COMICVINE_API_KEY")
COMICVINE_URL = "https://comicvine.gamespot.com/api/"
COMICVINE_TOTAL_CHARS = 100000


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

    if random.randint(0, 99) < 30:
        comicvine = True
    else:
        comicvine = False

    if waifu_manager.current_waifu_spawn is not None:
        if timers.get_time() - timers.get_waifu_claim_timer() < WAIFU_CLAIM_DELTA:
            return
        await waifu_manager.skip_waifu()
        claim_message = waifu_manager.claim_message
        old_embed = claim_message.embeds[0]
        desc = old_embed['description']
        desc += "\nClaimed by nobody. So sad."
        embed = discord.Embed(title=old_embed['title'], description=desc, color=old_embed['color'])
        await bot.edit_message(claim_message, embed=embed)
    if waifu_manager.is_prepared:
        response = waifu_manager.spawn_waifu()
        message = await bot.send_message(channel, embed=response)
        waifu_manager.set_claim_message(message)
        timers.set_waifu_claim_timer()
    while True:
        if comicvine:
            response = await get_random_comic_char()
            if response is not None:
                if not response['results'][0]['image']['medium_url'].endswith('blank.png'):
                    waifu_manager.prepare_comic_spawn(response)
                    return
        else:
            char_id = random.randint(1, 99999)
            response = await get_waifu_by_id(char_id)
            if response is not None:
                if response['image_url'] != DEFAULT_IMAGE_URL and response['member_favorites'] >= 5:
                    session = http_session.get_connection()
                    async with session.get(API_URL + "character/{}/pictures".format(response['mal_id'])) as resp:
                        pictures = await resp.json()
                    waifu_manager.prepare_waifu_spawn(response, pictures['pictures'])
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


async def get_random_comic_char():
    global COMICVINE_TOTAL_CHARS
    session = http_session.get_connection()
    params = {
        'api_key': COMICVINE_API_KEY,
        'format': 'json',
        'limit': 1,
        'offset': random.randint(0, COMICVINE_TOTAL_CHARS)
    }
    async with session.get(COMICVINE_URL + "characters", params=params) as resp:
        response = await resp.json()
    if response['error'] != "OK":
        return None
    COMICVINE_TOTAL_CHARS = int(response['number_of_total_results'])
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
    if is_correct_name(name, waifu_manager.current_waifu_spawn.name):
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
        result = await calculate_similarity(name, waifu_manager.current_waifu_spawn.name)
        if result > 5:
            await bot.add_reaction(ctx.message, '❌')
        else:
            await bot.say("You were off by {} letter{}.".format(result, 's' if result > 1 else ''))


def is_correct_name(guess, target):
    guess = guess.lower()
    target = target.lower()
    guess = guess.split(' ')
    target = target.split(' ')
    for word in target:
        if word not in guess:
            return False
    return True


async def calculate_similarity(guess, target):
    guess = guess.lower()
    guess = guess.split(' ')
    target = target.lower()
    target = target.split(' ')
    if len(target) != len(guess):
        return 99
    target_perms = [' '.join(x) for x in itertools.permutations(target)]
    min_result = 6
    for perm in target_perms:
        perm = perm.split(' ')
        result = 0
        groups = split_into_groups(list(itertools.product(perm, guess)), len(perm))
        for group in groups:
            min_group_result = 99999
            for words in group:
                if words[0][0] != words[1][0]:
                    continue
                mid_result = await calculate_word_similarity(words[1], words[0])
                if mid_result < min_group_result:
                    min_group_result = mid_result
            result += min_group_result
        if result < min_result:
            min_result = result
    return min_result


def split_into_groups(perms, num_of_words):
    result = [[] for x in range(len(perms) // num_of_words)]
    j = 0
    for i in range(len(perms)):
        if i != 0 and (i % num_of_words) == 0:
            j += 1
        result[j].append(perms[i])
    return result



async def calculate_word_similarity(guess, target):
    if guess == target:
        return 0
    matches = SequenceMatcher(None, guess, target).get_matching_blocks()
    size = 0
    for match in matches:
        size += match.size
    extra_letters = len(guess) - size
    return (len(target) - size) + extra_letters


@bot.command(pass_context=True)
async def skip(ctx):
    if ctx.message.author.id == "297869043640172545":
        await bot.say("Matthew no")
        return
    if ctx.message.author.id != "178887072864665600":
        await bot.say("You don't look like Zack to me.")
        return
    if waifu_manager.current_waifu_spawn is None:
        await bot.say("There's nothing to skip though 🤔")
        return
    await waifu_manager.skip_waifu()
    claim_message = waifu_manager.claim_message
    old_embed = claim_message.embeds[0]
    embed = discord.Embed(title=old_embed['title'], description="SKIPPED", color=old_embed['color'])
    await bot.edit_message(claim_message, embed=embed)


@bot.command(pass_context=True, name='list')
async def waifu_list(ctx, page: int=1):
    if page < 1:
        return
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
        if author.id == "266639261523116053":
            await bot.say("Aww, you didn't have to. You're the best ❤")
        else:
            await bot.say("Thanks! You are pretty cool yourself.")
    elif member.id == "178887072864665600":
        await bot.say("{}\nDad, you've been praised by {}. You're so popular.".format(member.mention, author.name))
    else:
        await bot.say("{}, you have been praised by {}! How nice of them!".format(member.mention, author.name))


@bot.command(pass_context=True)
async def schedule(ctx, day: str):
    day = day.lower()
    session = http_session.get_connection()
    async with session.get(API_URL + "schedule/{}".format(day)) as resp:
        response = await resp.json()
    embed = discord.Embed(title=day.capitalize(), color=0x09D3E3)
    for anime in response[day]:
        desc = ""
        episodes = "unknown" if anime.get('episodes', None) is None else str(anime['episodes'])
        desc += "**Episodes**: " + episodes
        desc += "\n"
        desc += "**Genres:** "
        for genre in anime['genres']:
            desc += "*{}* ".format(genre['name'])
        desc += "\n"
        desc += "Score: " + str(anime['score'])
        desc += "\n"
        desc += "Source: " + anime['source']
        embed.add_field(name="**" + anime['title'] + "**", value=desc, inline=False)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def insult(ctx, member: discord.Member):
    name = member.nick if member.nick is not None else member.name
    if member.id == bot.user.id:
        await bot.say("No u.")
        name = ctx.message.author.nick if ctx.message.author.nick is not None else ctx.message.author.name
    session = http_session.get_connection()
    params = {'who': name}
    async with session.get("https://insult.mattbas.org/api/insult", params=params) as resp:
            response = await resp.text()
    await bot.say(response)


@bot.command(pass_context=True)
async def compliment(ctx, member: discord.Member):
    if ctx.message.author.id == member.id:
        await bot.say("Complimenting yourself? That's sad. But hey, at least I like you.")
        return
    session = http_session.get_connection()
    async with session.get("https://complimentr.com/api") as resp:
            response = await resp.json()
    compliment = response["compliment"].capitalize() + "."
    await bot.say("{}\n{}".format(member.mention, compliment))
    if member.id == bot.user.id:
        await bot.say("Wow, thank you, {}!".format(ctx.message.author.mention))


@bot.command(pass_context=True)
async def say(ctx, channel_id: str, *args: str):
    channel = bot.get_channel(channel_id)
    msg = ' '.join(args)
    if ctx.message.author.id == "178887072864665600":
        await bot.send_message(channel, msg)
