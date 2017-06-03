import discord
from bot import bot
from GG import gg_manager as ggs


@bot.command(pass_context=True)
async def update_ggs(ctx):
    """Super secret bot owner only command."""
    if ctx.message.author.id != '178887072864665600':
        await bot.say("You're not kewl enough.")
        return
    for server in bot.servers:
        for member in server.members:
            ggs.add_user(member.id, member.name)

    await bot.say("Successfully updated.")


@bot.command(pass_context=True)
async def balance(ctx, member: discord.Member=None):
    """Check your money, yo."""
    if not member:
        member = ctx.message.author

    gg_balance = ggs.get_ggs(member.id)
    embed = discord.Embed()
    embed.add_field(name="{}'s balance".format(member.name), value=gg_balance)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def cheat(ctx, num: int, member: discord.Member):
    """You saw nothing."""
    if ctx.message.author.id != '178887072864665600':
        await bot.say("You're not kewl enough.")
        return

    if num >= 0:
        ggs.add(member.id, num)
    else:
        ggs.sub(member.id, num)
    current = ggs.get_ggs(member.id)
    await bot.say("{}'s balance is now: {} GGs.".format(member.name, current))
