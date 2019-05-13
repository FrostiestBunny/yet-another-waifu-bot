import discord
from discord.ext.commands import Cog, Context, NotOwner, command
from my_bot import MyBot
from player import players
from waifu_manager import waifu_manager
from timers import timers
import aiohttp
import asyncio
from http_session import http_session
import os


COMICVINE_API_KEY = os.getenv("COMICVINE_API_KEY")


class OwnerOnly(Cog, name="Owner Commands"):
    
    def __init__(self, bot: MyBot):
        self.bot = bot
        self.last_game = discord.Game("")
        self.last_status = discord.Status.online
    
    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, NotOwner):
            await ctx.send("You're not my dad.")
        raise error
    
    async def cog_check(self, ctx: Context):
        if await self.bot.is_owner(ctx.message.author):
            return True
        raise NotOwner

    @command()
    async def dismiss(self, ctx: Context):
        await ctx.message.add_reaction('👌')
        await self.bot.logout()
    
    @command()
    async def change_avatar(self, ctx: Context, url: str):
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar_b = await resp.read()
                await self.bot.edit_profile(avatar=avatar_b)
    
    @command()
    async def add_players(self, ctx: Context):
        guild = ctx.message.guild
        for member in guild.members:
            if not member.bot:
                players.add_player(member.id, member.name)
        await ctx.send("Updated player database")
    
    @command()
    async def say(self, ctx: Context, channel_id: int, *args: str):
        channel = self.bot.get_channel(channel_id)
        msg = ' '.join(args)
        if ctx.message.author.id == 178887072864665600:
            await channel.send(msg)
    
    @command()
    async def set_game(self, ctx: Context, *args):
        game_name = ' '.join(args)
        game = discord.Game(game_name)
        self.last_game = game
        await self.bot.change_presence(activity=game, status=self.last_status)
    
    @command()
    async def set_status(self, ctx: Context, status: str):
        states = {
            'online': discord.Status.online,
            'offline': discord.Status.offline,
            'idle': discord.Status.idle,
            'dnd': discord.Status.dnd
        }
        status = states.get(status, None)
        if status is None:
            await ctx.send("Uh, are you sure you're not going senile?")
            return
        self.last_status = status
        await self.bot.change_presence(activity=self.last_game, status=status)
    
    @command()
    async def cheat_spawn(self, ctx: Context, waifu_id: int):
        waifu_commands = self.bot.get_cog("Waifu Commands")
        response = await waifu_commands.get_waifu_by_id(waifu_id)
        pictures = await waifu_commands.get_mal_waifu_pics(waifu_id)
        waifu_manager.prepare_waifu_spawn(response, pictures['pictures'])
        embed = waifu_manager.spawn_waifu()
        message = await ctx.send(embed=embed)
        waifu_manager.set_claim_message(message)
        timers.set_waifu_claim_timer()
    
    @command()
    async def cheat_comic(self, ctx: Context, *args: str):
        waifu_commands = self.bot.get_cog("Waifu Commands")
        args = list(args)
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
        
        name = ' '.join(args)
        response = await waifu_commands.find_comicvine_char(name)
        
        embed = discord.Embed(title=name.capitalize(), color=0x09d3e3)
        for i, character in enumerate(response['results']):
            embed.add_field(name=f"{i+1}: **{character['name']}**",
                            value=f"Real name: {character['real_name']}",
                            inline=False)
        msg = await ctx.send(embed=embed)

        for i in range(len(response['results'])):
            await msg.add_reaction(r_map[i + 1])
        await msg.add_reaction("⏹")

        def check(reaction, user):
            e = str(reaction.emoji)
            return e.startswith(('1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '⏹')) and user.id == author.id\
                and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send("You didn't pick in time, too bad.")
            return
        await msg.delete()
        choice = None
        for k, v in r_map.items():
            if v == str(reaction.emoji):
                choice = k
                break
        
        if choice == "cancel":
            return

        url = response['results'][choice - 1]['api_detail_url']
        session = http_session.get_connection()
        params = {
            'api_key': COMICVINE_API_KEY,
            'format': 'json',
            'field_list': 'name,real_name,deck,image,site_detail_url,id'
        }
        async with session.get(url, params=params) as resp:
            response = await resp.json()

        waifu_manager.prepare_comic_spawn(response)
        embed = waifu_manager.spawn_waifu()
        message = await ctx.send(embed=embed)
        waifu_manager.set_claim_message(message)
        timers.set_waifu_claim_timer()
    
    @command()
    async def skip(self, ctx: Context):
        if waifu_manager.current_waifu_spawn is None:
            await ctx.send("There's nothing to skip though 🤔")
            return
        await waifu_manager.skip_waifu()
        claim_message = waifu_manager.claim_message
        old_embed = claim_message.embeds[0]
        embed = discord.Embed(title=old_embed.title, description="SKIPPED",
                              color=old_embed.color)
        await claim_message.edit(embed=embed)


def setup(bot: MyBot):
    c = OwnerOnly(bot)
    bot.add_cog(c)
