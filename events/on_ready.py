from discord.ext import commands, tasks
from itertools import cycle
from discord import Game, Status, app_commands
from addons.config import config


activities = cycle(config()["activity"])


class Ready(commands.Cog):
    """Shows that bot is ready and change status of bot"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status.start()

    @tasks.loop(seconds=60)
    async def status(self):
        await self.bot.wait_until_ready()
        await self.bot.change_presence(
            activity=Game(name=next(activities)), status=Status.dnd
        )

    @commands.Cog.listener()
    async def on_ready(self):
        for key in self.bot.all_commands:
            print("""Command Loaded : {}""".format(key))
        print(
            """Bot is online \nName: {} \nID: {} \nServers : {} \nCommands: {} Including aliases""".format(
                self.bot.user.name,
                self.bot.user.id,
                len(self.bot.guilds),
                len(self.bot.all_commands),
            )
        )
        x = await self.bot.tree.sync()
        print(x)
