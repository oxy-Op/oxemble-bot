from discord.ext import commands
from discord import app_commands, Interaction
from database.manage import Database
from addons.config import config
from database.manage import RedisCache
from addons.trackexec import track_speed
from asyncio import sleep
from time import time


class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.cache = RedisCache()

    @app_commands.command(name='balance', description='Shows your balance')
    @app_commands.checks.cooldown(1, 3)
    async def balance(self, interaction: Interaction):
        print("working1")
        self.db.connect()
        print("working2")
        balance = self.cache.get_data(f'user_balance:{interaction.user.id}')
        print("working3")
        if balance is None:
            balance = self.db.get_user_balance(interaction.user.id)
            self.cache.set_data(
                f"user_balance:{interaction.user.id}", balance, 180)
            balance = balance
        else:
            balance = balance.decode("utf-8")
        await interaction.response.send_message(interaction.user.mention + " " + config('balance') + f"**{str(balance)}** xembles")
        self.db.disconnect()

    @balance.error
    async def e(self, i: Interaction, e):
        if isinstance(e, app_commands.errors.CommandOnCooldown):
            unix = int(time() + e.retry_after)
            msg = await i.response.send_message(f'{i.user.mention} **{i.command.name} command is on cooldown for <t:{unix}:R>**')
            await sleep(int(e.retry_after))
            await i.delete_original_response()
