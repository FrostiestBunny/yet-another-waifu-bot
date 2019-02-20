import discord
from discord.ext.commands import command, Context
from io import BytesIO
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageOps


class ImageFun:

    def __init__(self, bot):
        self.bot = bot

    @command(pass_context=True)
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
        await self.bot.send_file(ctx.message.channel, fp=output, filename="uwot.png")
        output.close()


def setup(bot):
    cog = ImageFun(bot)
    bot.add_cog(cog)
