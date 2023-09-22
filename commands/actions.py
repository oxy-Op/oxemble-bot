import discord
import random
import requests
from discord.ext import commands
from addons.config import config


class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GIPHY_API_KEY = config()["giphy_api_key"]
        self.base_url = "https://api.giphy.com/v1/gifs/search"

    @commands.command()
    async def cuddle(self, ctx, user: discord.Member):
        action = "cuddle"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        action = "hug"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def kiss(self, ctx, user: discord.Member):
        action = "kiss"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def lick(self, ctx, user: discord.Member):
        action = "lick"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def pat(self, ctx, user: discord.Member):
        action = "pat"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def slap(self, ctx, user: discord.Member):
        action = "slap"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def stare(self, ctx, user: discord.Member):
        action = "stare"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def bite(self, ctx, user: discord.Member):
        action = "bite"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def greet(self, ctx, user: discord.Member):
        action = "greet"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def punch(self, ctx, user: discord.Member):
        action = "punch"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def tickle(self, ctx, user: discord.Member):
        action = "tickle"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def kill(self, ctx, user: discord.Member):
        action = "kill"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def pats(self, ctx, user: discord.Member):
        action = "pats"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def snuggle(self, ctx, user: discord.Member):
        action = "snuggle"
        await self._send_action_message(ctx, user, action)

    @commands.command()
    async def bully(self, ctx, user: discord.Member):
        action = "bully"
        await self._send_action_message(ctx, user, action)

    async def _send_action_message(self, ctx, user, action):
        url = f"{self.base_url}?api_key={self.GIPHY_API_KEY}&q=anime+{action}&limit=10&rating=pg-13&lang=en"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                gifs = data["data"]
                random_gif = random.choice(gifs)
                image_url = random_gif["images"]["original"]["url"]
                embed = discord.Embed()
                embed.description = f"{ctx.author.mention} {action}s {user.mention}"
                embed.set_image(url=image_url)
                embed.color = discord.Color(random.randint(0, 0xFFFFFF))
                await ctx.send(embed=embed)
            else:
                await ctx.send("No matching image found for the action.")
        else:
            await ctx.send("An error occurred while fetching the action image.")
