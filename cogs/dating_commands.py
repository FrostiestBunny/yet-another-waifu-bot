import discord
import asyncio
from discord.ext.commands import command, Context, Cog
from my_bot import MyBot
from date import DateBuilder, Choice


class DatingCommands(Cog, name="Dating Commands"):

    def __init__(self, bot: MyBot):
        self.bot = bot

    @command()
    async def test_date(self, ctx: Context):
        author = ctx.message.author
        r_map = {
            0: "0⃣",
            1: "1⃣",
            2: "2⃣",
            3: "3⃣",
            4: "4⃣",
            5: "5⃣",
            "cancel": "⏹"
        }

        builder = DateBuilder("dates.json")
        builder.start_build("test date")
        builder.add_text("You go on a date with [insert waifu here one day].\n")
        choice = Choice()
        choice.add_prompt("You find some money on the ground. Do you pick it up?")
        choice.add_option("yes", "Yes.")
        choice.add_option("no", "No.")
        choice.add_outcome("yes", "You get 50 bucks.")
        choice.add_outcome("no", "You're a loser and get nothing.")
        builder.add_choice(choice)
        date = builder.get_date("test date")

        text = date.main_text + choice.get_prompt()
        embed = discord.Embed(title="Test Date", color=0x09d3e3, description=text)
        i = 1
        options_map = {}
        for name, text in choice.get_options().items():
            embed.add_field(name=str(i), value=text, inline=False)
            options_map[i] = name
            i += 1
        
        msg = await ctx.send(embed=embed)

        for i in range(len(choice.get_options())):
            await msg.add_reaction(r_map[i + 1])
        await msg.add_reaction("⏹")

        def check(reaction, user):
            e = str(reaction.emoji)
            return e.startswith(('1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '⏹')) and user.id == author.id\
                and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=120)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send("You didn't pick in time, too bad.")
            return
        
        user_choice = None
        for k, v in r_map.items():
            if v == str(reaction.emoji):
                user_choice = k
                break
        
        if user_choice == "cancel":
            await msg.delete()
            await ctx.send("Bye then.")
            return
        
        user_choice = options_map[user_choice]
        outcome = choice.get_outcome(user_choice)
        desc = f"**Choice**: *{choice.get_options()[user_choice]}*\n{outcome}"
        embed = discord.Embed(title="Test Date", color=0x09d3e3, description=desc)
        await msg.edit(embed=embed)
        

def setup(bot: MyBot):
    cog = DatingCommands(bot)
    bot.add_cog(cog)
