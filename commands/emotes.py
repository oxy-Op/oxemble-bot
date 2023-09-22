import discord
from discord.ext import commands
import requests
import random
from addons.config import config


class Emotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giphy_api_key = config()["giphy_api_key"]
        self.base_url = "https://api.giphy.com/v1/gifs/search"

    @commands.command()
    async def blush(self, ctx):
        """Blush yourself"""
        await self.send_gif(ctx, " blush")

    @commands.command()
    async def cry(self, ctx):
        await self.send_gif(ctx, " cry")

    @commands.command()
    async def dance(self, ctx):
        await self.send_gif(ctx, " dance")

    @commands.command()
    async def lewd(self, ctx):
        await self.send_gif(ctx, " lewd")

    @commands.command()
    async def sleepy(self, ctx):
        await self.send_gif(ctx, " sleepy")

    @commands.command()
    async def smile(self, ctx):
        await self.send_gif(ctx, " smile")

    @commands.command()
    async def smug(self, ctx):
        await self.send_gif(ctx, " smug")

    @commands.command()
    async def thinking(self, ctx):
        await self.send_gif(ctx, " thinking")

    @commands.command()
    async def triggered(self, ctx):
        await self.send_gif(ctx, " triggered")

    @commands.command()
    async def happy(self, ctx):
        await self.send_gif(ctx, " happy")

    @commands.command()
    async def thumbs(self, ctx):
        await self.send_gif(ctx, " thumbs")

    @commands.command()
    async def grin(self, ctx):
        await self.send_gif(ctx, " grin")

    async def send_gif(self, ctx, query):
        url = f"{self.base_url}?api_key={self.giphy_api_key}&q=anime+{query}&limit=10&rating=pg-13&lang=en"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                gifs = data["data"]
                random_gif = random.choice(gifs)
                image_url = random_gif["images"]["original"]["url"]
                embed = discord.Embed()
                embed.set_image(url=image_url)
                embed.colour = discord.Colour.random()
                quote = self.get_random_quote()
                embed.title = f"{ctx.author.name} {query}"
                if quote:
                    embed.set_footer(text=quote)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Sorry, I couldn't find a GIF for that emote.")
        else:
            await ctx.send("Sorry, I couldn't retrieve the GIF.")

    def get_random_quote(self):
        return None
