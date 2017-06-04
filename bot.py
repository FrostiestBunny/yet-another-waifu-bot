# import discord
from discord.ext import commands
from GG import gg_manager as ggs
import random
import aiohttp


description = """It's gonna be kewl soon"""

bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print("Logged in")


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content == '\o':
        await bot.send_message(message.channel, 'o/')
    if random.randint(0, 99) < 5:
        author = message.author
        ggs.add(author.id, 10)


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
async def dismiss(ctx):
    """Put the bot to sleep."""
    if ctx.message.author.id == '178887072864665600':
        await bot.say("Going to sleep.")
        await bot.logout()
    else:
        await bot.say("You wish.")
        return
