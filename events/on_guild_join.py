from discord.ext import commands
from database.manage import Database


class GuildJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()  # Initialize your database connection here

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_id = guild.id
        members = guild.members
        for member in members:
            user_id = member.id
            if self.db.check_user_existence(user_id):
                self.db.add_user_to_guild(user_id, guild_id)
