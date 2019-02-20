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
        url = member.avatar_url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar = await resp.read()
        base = Image.open('images/uwot.png').convert('RGBA')
        av = Image.open(BytesIO(avatar)).convert('RGBA')
        av = ImageOps.fit(av, (260, 260))

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
        out.paste(av, box=(85, 360))
        output = BytesIO()
        out.save(output, format="PNG")
        output.seek(0)
        await self.bot.send_file(ctx.message.channel, fp=output, filename="uwot.png")
        output.close()


def setup(bot):
    cog = ImageFun(bot)
    bot.add_cog(cog)
