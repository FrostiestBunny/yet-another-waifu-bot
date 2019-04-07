import discord
from discord.ext.commands import Cog, Context, command, CheckFailure
from my_bot import MyBot


class NSFWOnly(Cog, name="NSFW Commands"):

    def __init__(self, bot: MyBot):
        self.bot = bot
    
    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, CheckFailure):
            await ctx.send(f"{ctx.message.channel.mention} isn't marked as NSFW.")
            return
        raise error
    
    async def cog_check(self, ctx: Context):
        channel = ctx.message.channel
        if channel.is_nsfw():
            return True
        raise CheckFailure("Channel isn't marked as NSFW")
    
    @command()
    async def test_nsfw(self, ctx: Context):
        await ctx.send("This seems a bit better.~~ *wink*")
        

def setup(bot: MyBot):
    c = NSFWOnly(bot)
    bot.add_cog(c)