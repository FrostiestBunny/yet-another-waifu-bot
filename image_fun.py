import discord
from io import StringIO, BytesIO
from bot import bot
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageOps


@bot.command(pass_context=True)
async def uwot(ctx, member: discord.Member, *args):
    url = member.avatar_url
    with aiohttp.ClientSession() as session:
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
    await bot.send_file(ctx.message.channel, fp=output, filename="uwot.png")
    output.close()
