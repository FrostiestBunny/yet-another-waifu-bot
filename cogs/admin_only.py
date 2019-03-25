import discord
from discord.ext.commands import Cog, Context, command, MissingPermissions
from my_bot import MyBot
from bot_config import bot_config


class AdminOnly(Cog, name="Admin Commands"):

    def __init__(self, bot: MyBot):
        self.bot = bot
    
    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"You don't have the necessary {error.missing_perms[0]} permission.")
            return
        raise error
    
    async def cog_check(self, ctx: Context):
        permissions = ctx.message.author.permissions_in(ctx.message.channel)
        if permissions.administrator:
            return True
        raise MissingPermissions(['administrator'])
    
    @command()
    async def set_spawn_channel(self, ctx: Context, channel: discord.TextChannel):
        bot_config.update_config('spawn_channel', str(channel.id))
        await ctx.send(f"Spawn channel set to {channel.mention}")
    
    @command()
    async def set_spawn_rate(self, ctx: Context, spawn_rate: int):
        bot_config.update_config('spawn_rate', spawn_rate)
        await ctx.send(f"Spawn rate set to {spawn_rate}% per message.")


def setup(bot: MyBot):
    c = AdminOnly(bot)
    bot.add_cog(c)
