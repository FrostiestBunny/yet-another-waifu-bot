import discord
from discord.ext.commands import Cog, Context, command
from my_bot import MyBot
from io import BytesIO
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageOps
from http_session import http_session


class MiscCommands(Cog, name="Misc Commands"):
    
    def __init__(self, bot: MyBot):
        self.bot = bot

    @command()
    async def suggest(self, ctx: Context, *args):
        suggestion = ' '.join(args)
        description = suggestion
        embed = discord.Embed(title=ctx.message.author.name, description=description,
                            color=0x0760FA)
        channel = await self.bot.get_suggestion_channel()
        message = await channel.send(embed=embed)
        await message.add_reaction(':yes_emoji:529842623532367872')
        await message.add_reaction(':no_emoji:529843815415021587')
        await ctx.message.add_reaction('👌')
    
    @command()
    async def gib_code(self, ctx: Context):
        await ctx.send("https://github.com/ZackUnfair/yet-another-waifu-bot")
    
    @command()
    async def uwot(self, ctx: Context, member: discord.Member, *args):
        author = ctx.message.author
        url = member.avatar_url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                target_avatar = await resp.read()
        url = author.avatar_url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                author_avatar = await resp.read()
        base = Image.open('images/uwot.png').convert('RGBA')
        target_av = Image.open(BytesIO(target_avatar)).convert('RGBA')
        target_av = ImageOps.fit(target_av, (260, 260))
        target_av2 = Image.open(BytesIO(target_avatar)).convert('RGBA')
        target_av2 = ImageOps.fit(target_av2, (114, 114))
        author_av = Image.open(BytesIO(author_avatar)).convert('RGBA')
        author_av = ImageOps.fit(author_av, (122, 122))

        txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

        fnt = ImageFont.truetype('fonts/big_noodle_titling.ttf', 20)
        d = ImageDraw.Draw(txt)

        res = ""
        for a in args:
            res += a
            res += " "

        d.text((455, 450), res, font=fnt, fill=(0, 0, 0, 255))

        txt = txt.rotate(-25, resample=Image.BILINEAR)
        out = Image.alpha_composite(base, txt)
        out.paste(target_av, box=(85, 360))
        out.paste(author_av, box=(116, 33))
        out.paste(target_av2, box=(477, 8))
        output = BytesIO()
        out.save(output, format="PNG")
        output.seek(0)
        f = discord.File(output, 'uwot.png')
        await ctx.send(file=f)
        output.close()
    
    @command()
    async def insult(self, ctx: Context, member: discord.Member):
        name = member.nick if member.nick is not None else member.name
        author = ctx.message.author
        if member.id == self.bot.user.id:
            await ctx.send("No u.")
            name = author.nick if author.nick is not None else author.name
        session = http_session.get_connection()
        params = {'who': name}
        async with session.get("https://insult.mattbas.org/api/insult", params=params) as resp:
            response = await resp.text()
        await ctx.send(response)
    @command()
    async def rip_zack(self, ctx: Context):
        await ctx.send("May one day dad come back to life.")

def setup(bot: MyBot):
    c = MiscCommands(bot)
    bot.add_cog(c)
