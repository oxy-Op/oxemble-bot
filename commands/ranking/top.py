from discord.ext import commands
from discord import app_commands, Interaction, Embed, Color
from database.manage import Database
from database.manage import RedisCache
from addons.trackexec import track_speed
from asyncio import sleep
from time import time


class Top(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.cache = RedisCache()
        self.color = Color.blue()

    @app_commands.command(name="top", description="Display top guild ranking")
    @app_commands.checks.cooldown(1, 30)
    @app_commands.choices(category=[app_commands.Choice(name="balance", value=1)])
    async def top(self, interaction: Interaction, category: app_commands.Choice[int]):
        if category.value == 1:
            members = self.cache.smembers(f"guild:{interaction.guild.id}:users")
            if len(members) == 0:
                members = []
                for member in interaction.guild.members:
                    if not member.bot:
                        if self.db.check_user_existence(member.id):
                            key = f"guild:{interaction.guild.id}:users"
                            self.cache.sadd(key, member.id)
                            self.cache.expire(key, 1000)
                            members.append(member.id)
                print(members, 1)
            else:
                members = members

            user_ids = []
            for i in members:
                if isinstance(i, bytes):
                    user_ids.append(i.decode("utf-8"))
                else:
                    user_ids.append(i)

            top = self.db.get_user_balances(user_ids)
            user_id = interaction.user.id
            top_fields = []
            for u_rank, (u_id, balance) in enumerate(top, start=1):
                user = self.bot.get_user(u_id)
                if user is not None:
                    if u_id == user_id:
                        field_name = f"#{u_rank} {user.name}"
                        field_value = f"Balance: **{balance} xembles**"
                    else:
                        field_name = f"#{u_rank} {user.name}"
                        field_value = f"Balance: **{balance} xembles**"
                    top_fields.append((field_name, field_value))
                else:
                    top_fields.append(
                        (f"#{u_rank} Unknown User", f"Balance: {balance}")
                    )

            embed = Embed(
                title=f"Top Balance - {interaction.guild.name}",
                color=self.color,
            )

            for field_name, field_value in top_fields:
                embed.add_field(name=field_name, value=field_value, inline=False)

            embed.set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar,
            )

            await interaction.response.send_message(embed=embed)

    @top.error
    async def e(self, i: Interaction, e):
        if isinstance(e, app_commands.errors.CommandOnCooldown):
            unix = int(time() + e.retry_after)
            await i.response.send_message(
                f"{i.user.mention} **{i.command.name} command is on cooldown for <t:{unix}:R>**"
            )
            await sleep(int(e.retry_after))
            await i.delete_original_response()
