from discord.ext import commands
from discord import app_commands, Interaction
from asyncio import sleep
from time import time


class AppError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """An Error Handler for commands"""

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            print('xerrr')
            unix = int(time() + error.retry_after)
            er = await interaction.response.send_message(f'{interaction.user.mention} **{interaction.command.name} command is on cooldown for <t:{unix}:R> **')
            return
        elif isinstance(error, app_commands.CommandNotFound):
            await interaction.response.send_message("Command not found")
        elif isinstance(error, app_commands.BotMissingPermissions):
            await interaction.response.send_message('It looks like I dont have permission to execute this command. Please check my role position and permissions')
        else:
            raise (error)
