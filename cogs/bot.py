import discord
from discord.ext.commands import command, Context
import aiohttp
from http_session import http_session


class BotCommands:

    def __init__(self, bot):
        self.bot = bot

    @command(pass_context=True)
    async def change_avatar(self, ctx: Context, url: str):
        if ctx.message.author.id != '178887072864665600':
            await self.bot.say("You're not Zack enough.")
            return
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar_b = await resp.read()
                await self.bot.edit_profile(avatar=avatar_b)

    @command(pass_context=True)
    async def word_ratio(self, ctx: Context, word, user: discord.Member, message_limit=None):

        message_counter = 0
        word_counter = 0
        for message in self.bot.messages:
            if message.author == user:
                message_counter += 1
                message_content = message.content.lower()
                count = message_content.count(word.lower())
                word_counter += count
            if message_limit is not None and message_counter == message_limit:
                break
        if message_counter == 0:
            await self.bot.say(
                f"{user.name} didn't say anything in the last {message_counter} messages.")
            return

        if word_counter == 0:
            await self.bot.say("{} didn't mention the word even once.".format(user.name))
            return
        ratio = word_counter / message_counter
        await self.bot.say(
            "{}'s ratio of {} per message in the last {} messages is:\n {:.2f}".format(
                user.name, word, message_counter, ratio))

    @command(pass_context=True)
    async def dismiss(self, ctx: Context):
        """Put the bot to sleep."""
        if ctx.message.author.id == '178887072864665600':
            await http_session.close()
            await self.bot.add_reaction(ctx.message, '👌')
            await self.bot.logout()
        else:
            await self.bot.say("You wish.")
            return

    @command(pass_context=True)
    async def gib_code(self, ctx: Context):
        await self.bot.say("https://github.com/ZackUnfair/yet-another-waifu-bot")


def setup(bot):
    cog = BotCommands(bot)
    bot.add_cog(cog)
