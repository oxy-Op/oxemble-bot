from discord.ext import commands
from discord.embeds import Embed
from discord import __version__
import os
from addons.config import config


class Info(commands.Cog):
    """An Info command for bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["about", "botinfo"])
    async def _info(self, ctx):
        owner = await self.bot.fetch_user(config()["owner_id"])
        embed = Embed(title="Information about bot", color=0x55EEFF)
        embed.add_field(name="Name", value=self.bot.user.name)
        embed.add_field(name="ID", value=self.bot.user.id)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.add_field(name="Owner", value=owner.name)
        embed.add_field(name="Programmer", value=owner.name)
        embed.add_field(
            name="Programming Language", value=os.system("python --version")
        )
        embed.add_field(name="API Wrapper", value="discord {}".format(__version__))
        await ctx.send(embed=embed)
