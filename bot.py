import discord
from discord.ext import commands
import asyncio
import logging
from addons.config import config

logging.basicConfig(
    level=logging.ERROR, format="[%(asctime)s] [%(levelname)s] %(message)s"
)
config = config()


class Oxemble(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def process_commands(self, message):
        await super().process_commands(message)


bot = Oxemble(
    command_prefix=config["prefix"],
    help_command=None,
    case_insensitive=True,
    strip_after_prefix=True,
    intents=discord.Intents.all(),
    self_bot=False,
)


async def Init():
    async with bot:
        await bot.load_extension("commands.gamble.__init__")
        await bot.load_extension("commands.__init__")
        await bot.load_extension("events.__init__")
        await bot.start(config["token"])


if __name__ == "__main__":
    asyncio.run(Init())
