# import discord
from discord.ext import commands


description = """It's gonna be kewl soon"""

bot = commands.Bot(command_prefix='?', description=description)


@bot.event
async def on_ready():
    print("Logged in")


@bot.event
async def on_message(message):
    if message.content == '\o':
        await bot.send_message(message.channel, 'o/')
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
