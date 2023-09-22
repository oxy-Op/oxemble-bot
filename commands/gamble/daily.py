from discord.ext import commands
from discord import app_commands, Interaction
from database.manage import Database
from database.manage import RedisCache
from addons.trackexec import track_speed
from asyncio import sleep
from time import time
from random import randint, random
from datetime import timedelta


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.cache = RedisCache()

    @app_commands.command(name='daily', description='Daily xembles')
    @app_commands.checks.cooldown(1, 3600)
    @track_speed
    async def dailyx(self, i: Interaction):
        user_id = i.user.id
        last_claim_time = self.db.get_last_claim_time(user_id)
        current_time = time()
        time_elapsed = current_time - last_claim_time
        if time_elapsed >= 86400:  # 24 hours in seconds
            daily_balance = randint(100, 1000)
            self.db.connect()
            self.db.increment_user_balance(user_id, daily_balance)
            self.cache.increment_balance(
                f"user_balance:{user_id}", daily_balance)
            self.db.update_last_claim_time(user_id, current_time)
            await i.response.send_message(f"You received {daily_balance} daily xembles")
            self.db.disconnect()
        else:
            time_remaining = 86400 - time_elapsed
            response = f"You can claim your daily balance in {str(timedelta(seconds=time_remaining))}."
            await i.response.send_message(response, ephemeral=True)

    @dailyx.error
    async def e(self, i: Interaction, e):
        if isinstance(e, app_commands.errors.CommandOnCooldown):
            unix = int(time() + e.retry_after)
            msg = await i.response.send_message(f'{i.user.mention} **{i.command.name} command is on cooldown for <t:{unix}:R>**')
            await sleep(4)
            await i.delete_original_response()
