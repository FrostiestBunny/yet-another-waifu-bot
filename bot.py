# import discord
from discord.ext import commands
from GG import gg_manager as ggs
import random


description = """It's gonna be kewl soon"""

bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print("Logged in")


@bot.event
async def on_message(message):
    if message.content == '\o':
        await bot.send_message(message.channel, 'o/')
    if random.randint(0, 99) < 10:
        author = message.author
        ggs.add(author.id, 15)
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def dismiss(ctx):
    """Put the bot to sleep."""
    if ctx.message.author.id == '178887072864665600':
        await bot.say("Going to sleep.")
        await bot.logout()
    else:
        await bot.say("You wish.")
        return
