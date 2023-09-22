import discord
from discord.ext import commands


class UserInfo(commands.Cog):
    """An command that shows user information \n
    parameters:
    `discord.Member`: User mentioned if not then command executer will be triggered
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo', aliases=['user', 'whois', 'infouser'])
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        em = discord.Embed(description=user.mention)
        em.set_author(name=str(user), icon_url=user.avatar)
        em.set_thumbnail(url=user.avatar)
        em.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        em.add_field(name="Join position", value=str(members.index(user) + 1))
        em.add_field(name="Registered",
                     value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            em.add_field(name="Roles [{}]".format(len(user.roles) - 1),
                         value=role_string,
                         inline=False)
        perm_string = ', '.join([
            str(p[0]).replace("_", " ").title() for p in user.guild_permissions
            if p[1]
        ])
        em.add_field(name="Guild permissions", value=perm_string, inline=False)
        em.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=em)


