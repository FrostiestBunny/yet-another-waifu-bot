import discord
from bot import bot
from GG import gg_manager as ggs


@bot.event
async def on_server_join(server):
        for member in server.members:
            ggs.add_user(member.id, member.name)


@bot.command(pass_context=True)
async def update_db_cause_zack_sucks(ctx):
    if ctx.message.author.id != '178887072864665600':
        await bot.say("You're not Zack enough.")
        return
    for server in bot.servers:
        for member in server.members:
            ggs.add_user(member.id, member.name)
    await bot.say("Successfully updated the database. Git gud Zack, seriously.")


@bot.command(pass_context=True)
async def reset_db(ctx):
    if ctx.message.author.id != '178887072864665600':
        await bot.say("You're not Zack enough.")
        return
    for server in bot.servers:
        for member in server.members:
            ggs.set(member.id, 10)
    await bot.say("Successfully updated the database. Git gud Zack, seriously.")


@bot.command(pass_context=True)
async def transfer(ctx, member: discord.Member, num: int):
    """Transfer GGs to other users."""
    if member.bot:
        await bot.say("You're a bot, mate.")
        return
    if num <= 0:
        await bot.say("Haha, good one, mate.")
        return
    sender = ctx.message.author
    sender_ggs = ggs.get_ggs(sender.id)
    if sender_ggs < num:
        await bot.say("You don't even have that much, scrub.")
        return
    ggs.add(member.id, num)
    ggs.sub(sender.id, num)
    await bot.say("Successfully transferred {} GGs to {}.".format(num, member.name))


@bot.command(pass_context=True)
async def balance(ctx, member: discord.Member=None):
    """Check your money, yo."""
    if member is None:
        member = ctx.message.author

    gg_balance = ggs.get_ggs(member.id)
    embed = discord.Embed()
    embed.add_field(name="{}'s balance".format(member.name), value=str(gg_balance)+" GGs.")
    await bot.say(embed=embed)


@bot.command()
async def top():
    users = (ggs.ggs_data.keys())
    users = sorted(users, key=lambda u: ggs.get_ggs(u), reverse=True)
    users = users[:10]
    result = ""
    for user in users:
        u_data = ggs.get_user(user)
        result += "{} - {}\n".format(u_data['name'], u_data['ggs'])
    embed = discord.Embed()
    embed.add_field(name="Top 10", value=result)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def cheat(ctx, num: int, *members: discord.Member):
    """You saw nothing."""
    author = ctx.message.author
    roles = map(str, author.roles)
    if 'Bot Commander' in roles or author.id == '178887072864665600':
        for member in members:
            if num >= 0:
                ggs.add(member.id, num)
            else:
                ggs.sub(member.id, num)
        await bot.say("Added {} GGs.".format(num))
    else:
        await bot.say("You're not kewl enough.")
        return
