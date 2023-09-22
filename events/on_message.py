from discord import DMChannel
from discord.embeds import Embed
from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, DMChannel):
            return
        if message.content == '<@!799595001797279754>':
            embed = Embed(
                description='Prefix :-  `{}`'.format(self.bot.command_prefix))
            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Message(bot))
