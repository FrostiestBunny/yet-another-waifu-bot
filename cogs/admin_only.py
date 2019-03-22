import discord
from discord.ext.commands import Cog, Context, command, MissingPermissions
from my_bot import MyBot
from bot_config import bot_config


class AdminOnly(Cog, name="Admin Commands"):

    def __init__(self, bot: MyBot):
        self.bot = bot
    
    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have the necessary permissions.")
        raise error
    
    async def cog_check(self, ctx: Context):
        permissions = ctx.message.author.permissions_in(ctx.message.channel)
        if permissions.administrator:
            return True
        raise MissingPermissions
    
    @command()
    async def set_spawn_channel(self, ctx: Context, channel: discord.TextChannel):
        bot_config.update_config(channel.id)
        await ctx.send("Spawn channel set to {}".format(channel.mention))


def setup(bot: MyBot):
    c = AdminOnly(bot)
    bot.add_cog(c)
