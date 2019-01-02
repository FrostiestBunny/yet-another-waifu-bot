import discord
from discord.ext import commands
from GG import gg_manager
import random
import aiohttp


description = """It's gonna be kewl soon"""

bot = commands.Bot(command_prefix='?', description=description)


@bot.command(pass_context=True)
async def change_avatar(ctx, url: str):
    if ctx.message.author.id != '178887072864665600':
        await bot.say("You're not Zack enough.")
        return
    with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            avatar_b = await resp.read()
            await bot.edit_profile(avatar=avatar_b)


@bot.command(pass_context=True)
async def word_ratio(ctx, word, user: discord.Member, message_limit=None):

    message_counter = 0
    word_counter = 0
    for message in bot.messages:
        if message.author == user:
            message_counter += 1
            message_content = message.content.lower()
            count = message_content.count(word.lower())
            word_counter += count
        if message_limit is not None and message_counter == message_limit:
            break
    if message_counter == 0:
        await bot.say("{} didn't say anything in the last {} messages.".format(user.name, message_counter))
        return

    if word_counter == 0:
        await bot.say("{} didn't mention the word even once.".format(user.name))
        return
    ratio = word_counter / message_counter
    await bot.say("{}'s ratio of {} per message in the last {} messages is:\n {:.2f}".format(
        user.name, word, message_counter, ratio))


@bot.command(pass_context=True)
async def dismiss(ctx):
    """Put the bot to sleep."""
    if ctx.message.author.id == '178887072864665600':
        gg_manager.close()
        await bot.say("Going to sleep.")
        await bot.logout()
    else:
        await bot.say("You wish.")
        return
