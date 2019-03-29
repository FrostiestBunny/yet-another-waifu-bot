import discord
from discord.ext.commands import command, Context, Cog
from http_session import http_session
import random
import os
from my_bot import MyBot


class CuteCommands(Cog, name="Cute Commands"):

    def __init__(self, bot: MyBot):
        self.bot = bot
        self.newt_id = 266639261523116053
        self.zack_id = 178887072864665600
    
    @command()
    async def praise(self, ctx: Context, member: discord.Member):
        author = ctx.message.author
        if member.id == author.id:
            await ctx.send("Praising yourself? How sad.\n*pats*")
        elif member.id == self.bot.user.id:
            if author.id == self.newt_id:
                await ctx.send("Aww, you didn't have to. You're the best ❤")
            else:
                await ctx.send("Thanks! You are pretty cool yourself.")
        elif member.id == self.zack_id:
            await ctx.send(
                f"{member.mention}\nDad, {author.name} praised you. You're so popular.")
        else:
            await ctx.send(
                f"{member.mention}, you have been praised by {author.name}! How nice of them!")
    
    @command()
    async def compliment(self, ctx: Context, member: discord.Member):
        if ctx.message.author.id == member.id:
            await ctx.send(
                "Complimenting yourself? That's sad. But hey, at least I like you.")
            return
        session = http_session.get_connection()
        async with session.get("https://complimentr.com/api") as resp:
            response = await resp.json()
        compliment = response["compliment"].capitalize() + "."
        await ctx.send("{}\n{}".format(member.mention, compliment))
        if member.id == self.bot.user.id:
            if ctx.message.author.id == self.newt_id:
                await ctx.send("*blushes*\nThanks Newt! ❤")
            else:
                await ctx.send("Wow, thank you, {}!".format(ctx.message.author.mention))
    
    @command()
    async def hug(self, ctx: Context, member: discord.Member):
        author = ctx.message.author
        if member.id == author.id:
            await ctx.send("How does that work? 🤔")
            return
        if member.id == self.bot.user.id:
            if author.id not in [self.zack_id, self.newt_id]:
                await ctx.send("Uh, sorry, but no.")
                return
        gif_name = random.choice(os.listdir('images/hugs'))
        with open(f'images/hugs/{gif_name}', "rb") as gif:
            msg = f"{ctx.message.author.mention} hugs {member.mention}"
            f = discord.File(gif, "hug.gif")
            await ctx.send(content=msg, file=f)
    
    @command(aliases=['pat'])
    async def headpat(self, ctx: Context, member: discord.Member):
        author = ctx.message.author
        gif_name = random.choice(os.listdir('images/headpats'))
        gif = open(f'images/headpats/{gif_name}', "rb")
        f = discord.File(gif, "headpat.gif")
        if author.id == member.id:
            msg = f"Feeling lonely, {author.mention}? *pats*"
        elif member.id == self.bot.user.id:
            if author.id == self.zack_id or author.id == self.newt_id:
                msg = "*gets patted*\nAww, thanks~~"
            else:
                await ctx.send("Uh, sorry, I don't think we're close enough.")
                return
        else:
            msg = f"*{author.mention} pats {member.mention}'s head*"
        await ctx.send(content=msg, file=f)
        gif.close()


def setup(bot: MyBot):
    cog = CuteCommands(bot)
    bot.add_cog(cog)
