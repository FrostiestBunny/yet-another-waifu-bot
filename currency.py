import discord
from bot import bot
from GG import gg_manager as ggs
from person import people
from random import randint, choice


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
    """Display ten richest users."""
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


@bot.command(pass_context=True)
async def get_pimp(ctx, member: discord.Member):
    author = ctx.message.author
    if member is None:
        await bot.say("No such member.")
        return
    if people.get_pimp(author.id) is not None:
        await bot.say("You're a pimp, mate, can't be a whore too.")
        return
    worker = people.get_worker(author.id)
    if people.get_worker(member.id):
        await bot.say("That person is already a slut, too bad.")
        return
    if worker is None:
        await bot.say("You're not a registered slut, please use the ?prostitute command first, then this one.")
        return
    if worker.has_pimp():
        await bot.say("You already have a pimp.")
        return

    await bot.say("{}, {} wants you to be their pimp, do you accept? Being their pimp means you get a part of their " +
                  "earnings, but you'll have the burden of protecting them. Also you can't become a slut as a pimp."
                  .format(member.mention, author.name))
    resp = await bot.wait_for_message(author=member, timeout=120)
    if resp is None:
        await bot.say("Waited too long, aborting.")
        return
    if 'yes' in resp.content.lower():
        pimp = people.get_pimp(member.id)
        if pimp is None:
            if len(people.pimps) == 5:
                await bot.say("Reached limit of pimps, use one that already exists.")
                return
            people.add_pimp(member.id, member.name)
            pimp = people.get_pimp(member.id)
        worker.add_pimp(pimp)
        await bot.say("{} is now your pimp, {}, congratulations. You can now use the ?prostitute command."
                      .format(member.name, author.mention))
        return
    else:
        await bot.say("Welp, too bad. You'll need to find somebody else, {}.".format(author.name))
        return


@bot.command(pass_context=True)
async def slut(ctx):
    author = ctx.message.author
    if people.get_pimp(author.id) is not None:
        await bot.say("You're a pimp, mate, can't be a whore too.")
        return
    if people.get_worker(author.id) is None:
        await bot.say("You don't seem to be registered as a prostitute. Do you want to become one?")
        resp = await bot.wait_for_message(author=author, timeout=120)
        if resp is None:
            await bot.say("Waited too long, aborting.")
            return
        if 'yes' in resp.content.lower():
            people.add_worker(author.id, author.name)
            await bot.say("Alright, now you'll need a pimp." +
                          " Please use the ?get_pimp command with the username of the person you want as your pimp." +
                          " There is a limit of 5 pimps in total.")
            return

        else:
            await bot.say("Alrighty then. No means no.")
            return
    worker = people.get_worker(author.id)
    if not worker.has_pimp():
        await bot.say("You don't have a pimp, use the ?get_pimp command.")
        return

    if worker.check_time(30 * 60):
        worker.set_time()
        pick = randint(1, 5)
        pimp = worker.get_pimp()

        if pick == 1:
            number = randint(50, 350)
            number2 = 0.3 * number
            ggs.add(author.id, number - number2)
            ggs.add(pimp.ide, number2)
            await bot.say("You had a poor client and earned {} GGs in total. {} goes to you, and {} to your pimp."
                          .format(number, number - number2, number2))
        elif pick == 2:
            number = randint(100, 500)
            number2 = 0.3 * number
            ggs.add(author.id, number - number2)
            ggs.add(pimp.ide, number2)
            member = choice(list(ctx.message.server.members))
            while member.name == author.name:
                member = choice(list(ctx.message.server.members))
            await bot.say("You had {} as your client and earned {} GGs in total. {} goes to you, and {} to your pimp."
                          .format(member.name, number, number - number2, number2))
        elif pick == 3:
            number = randint(150, 650)
            number2 = 0.3 * number
            ggs.add(author.id, number - number2)
            ggs.add(pimp.ide, number2)
            await bot.say("You had a wealthy client and earned {} GGs in total. {} goes to you, and {} to your pimp."
                          .format(number, number - number2, number2))
        elif pick == 4:
            gg = ggs.get_ggs(author.id)
            number = randint(50, max(gg * 1/3, 100))
            ggs.sub(author.id, number)
            await bot.say("You got caught and fined for {} GGs."
                          .format(number))
        elif pick == 5:
            gg = ggs.get_ggs(pimp.ide)
            number = randint(50, max(gg * 1 / 3, 100))
            ggs.sub(pimp.ide, number)
            await bot.say("You trespassed on another pimp's territory. It costs your pimp, {},  {} GGs."
                          .format(pimp.mention, number))

    else:
        time_left = worker.time_left()
        if time_left >= 60:
            time = time_left // 60
            await bot.say("You must wait {} minutes.".format(time))
        else:
            time = time_left
            await bot.say("You must wait {} seconds.".format(time))
        return
