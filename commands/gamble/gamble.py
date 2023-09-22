from random import choice
from discord import Color, Embed, app_commands, Interaction
from discord.ext import commands
from database.manage import RedisCache, Database
from addons.trackexec import track_speed
from asyncio import sleep
from addons.config import config
from time import time


class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = RedisCache()
        self.color = Color.red()
        self.db = Database()

    @app_commands.command(name='gamble', description="Gamble your amount")
    @app_commands.checks.cooldown(2, 5)
    @track_speed
    async def gamblex(self, i: Interaction, amount: app_commands.Range[int, 1, 10000]):
        user_id = i.user.id
        if amount < 0:
            return
        if amount > 10000:
            await i.response.send_message("Maximum amount to gamble is 10000 xembles")
        if amount == 0:
            usage_embed = Embed(
                title="Gamble Command",
                description=f"Usage: `/{i.command.name} <amount>`",
                color=self.color
            )
            usage_embed.set_footer(
                text=f"Requested by {i.user.name}", icon_url=i.user.avatar)
            await i.response.send_message(embed=usage_embed)

        if amount > 0:
            balance = self.cache.get_data(f"user_balance:{i.user.id}")
            if balance is None:
                balance = self.db.get_user_balance(i.user.id)
                self.cache.set_data(f"user_balance:{i.user.id}", balance)
                balance = int(balance)
            else:
                balance = int(balance.decode("utf-8"))

            if amount > balance:
                await i.response.send_message(f"{i.user.mention}, your current balance is lower than the bet amount")
                await sleep(1)
                await i.delete_original_response()
                return

            elif amount <= balance:
                choices = ["head", "tail"]
                chosen_side = choice(choices)
                emoji = config('emoji')
                await i.response.send_message(f"{i.user.mention} **bets** {amount} {emoji[0]} xembles")
                for _ in emoji:
                    content = f'{i.user.mention} **bets** {amount} {_} xembles'
                    await i.edit_original_response(content=content)
                    await sleep(1)

                if chosen_side == "head":
                    balance += amount
                    self.db.update_user_balance(i.user.id, balance)
                    self.cache.set_data(
                        f"user_balance:{user_id}", str(balance), 1000)
                    await i.edit_original_response(content=f"Congratulations! {i.user.mention} You won! Your new balance is **" + str(balance) + "**" + " xembles")
                else:
                    ne_balance = balance - amount
                    self.db.update_user_balance(i.user.id, ne_balance)
                    await i.edit_original_response(content=f"{i.user.mention} You **lost** the gamble. Better luck next time!")
                    self.cache.set_data(
                        f"user_balance:{user_id}", str(ne_balance), 1000)

    @gamblex.error
    async def e(self, i: Interaction, e):
        if isinstance(e, app_commands.errors.CommandOnCooldown):
            unix = int(time() + e.retry_after)
            msg = await i.response.send_message(f'{i.user.mention} **{i.command.name} command is on cooldown for <t:{unix}:R>**')
            await sleep(int(e.retry_after))
            await i.delete_original_response()
