from discord.ext import commands
from discord.embeds import Embed


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def _ping(self, ctx):
        embed = Embed()
        embed.title = 'Ping!'
        embed.description = f"Pong! {round(self.bot.latency * 1000)}ms"
        embed.color = 0xaee123
        await ctx.send(embed=embed)


