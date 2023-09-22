from discord.ext import commands
from discord.embeds import Embed


class Invite(commands.Cog):
    """Sends Invitation link of the bot"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='invite', aliases=['inv'])
    async def _invite(self, ctx):
        embed = Embed(title="Invitation",
                      description='[Click Here to invite](https://discord.com/api/oauth2/authorize?client_id={}&permissions=268561646&scope=bot) \n \n'.format(self.bot.user.id), color=0xff44ff)
        await ctx.send(embed=embed)


