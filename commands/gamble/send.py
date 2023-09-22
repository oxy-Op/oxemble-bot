from discord.ext import commands
from database.manage import Database
from addons.config import config
from database.manage import RedisCache
from addons.trackexec import track_speed
from discord import User, Embed, Color, Interaction, app_commands
from asyncio import sleep
from time import time

class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.cache = RedisCache()
        self.color = Color.blue()

    @app_commands.command(name='send', description='Send xembles to others')
    @app_commands.checks.cooldown(1, 10)
    @track_speed
    async def sendx(self, i: Interaction, user: User, amount: int):
        if amount < 0:
            return
        if amount > 100000:
            await i.response.send_message("Maximum amount to send is 100000 xembles")
        if i.user == user:
            return
        if user.bot:
            return
        if user == self.bot.user:
            return
        if amount == 0:
            usage_embed = Embed(
                title="Send Command",
                description=f"Usage: `/{i.command.name} <@user> <amount>`",
                color=self.color
            )
            usage_embed.set_footer(
                text=f"Requested by {i.user.name}", icon_url=i.user.avatar)
            await i.response.send_message(embed=usage_embed)
            return

        if amount > 0:
            if not self.db.check_user_existence(user.id):
                await i.response.send_message("User is not registered")
                return
            balance = self.cache.get_data(f"user_balance:{i.user.id}")
            if balance is None:
                balance = self.db.get_user_balance(i.user.id)
                balance = int(balance)
            else:
                balance = int(balance.decode("utf-8"))

            if amount > balance:
                await i.response.send_message(f"{i.user.mention}, you currently do not possess **{amount}** xembles to send")
                self.cache.set_data(f"user_balance:{i.user.id}", balance)
                await sleep(4)
                await i.delete_original_response()

            elif amount <= balance:
                x = self.db.transfer_balance(i.user.id, user.id, amount)
                y, z = x
                self.cache.transfer_balance(i.user.id, user.id, y, z, 120)
                embed = Embed(
                    title="Successful Transfer",
                    description=f"{i.user.mention} sent **{amount} xembles** to {user.mention}!",
                    color=self.color,
                )
                await i.response.send_message(content=user.mention,embed=embed)

    @sendx.error
    async def e(self, i: Interaction, e):
        if isinstance(e, app_commands.errors.CommandOnCooldown):
            unix = int(time() + e.retry_after)
            await i.response.send_message(f'{i.user.mention} **{i.command.name} command is on cooldown for <t:{unix}:R>**')
            await sleep(int(e.retry_after))
            await i.delete_original_response()
