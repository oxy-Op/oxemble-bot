from discord.ext import commands
from discord.embeds import Embed


class ServerInfo(commands.Cog):
    """Shows information about server"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='serverinfo', aliases=['server', 'guild', 'infoserver'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def serverinfo(self, ctx):
        try:
            server = ctx.guild
            embed = Embed(title="Server Information", color=0xabcdef)
            embed.add_field(name="Name", value=server.name)
            embed.add_field(name="ID", value=server.id)
            embed.add_field(name="Owner", value=server.owner)
            embed.add_field(name="Total Members", value=(server.member_count))
            embed.add_field(name="Channels Count",
                            value=len(server.text_channels))
            embed.add_field(name="Voice channels count",
                            value=len(server.voice_channels))
            embed.add_field(name="Roles Count", value=len(server.roles))
            embed.add_field(name="Total Emojis", value=len(server.emojis))
            embed.add_field(name="Total Boosts",
                            value=server.premium_subscription_count)
            embed.add_field(name="Boost Level", value=server.premium_tier)
            embed.add_field(name="Features",
                            value=server.features, inline=False)
            embed.add_field(name="Server Created at ", value=server.created_at)
            # embed.set_thumbnail(url=server.icon_url)
            embed.set_footer(text="Message Requested by " + ctx.author.name +
                             "#" + ctx.author.discriminator, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

