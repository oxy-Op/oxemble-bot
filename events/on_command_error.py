from discord.ext import commands
from asyncio import sleep
from time import time


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """An Error Handler for commands"""

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            unix = int(time() + error.retry_after)
            er = await ctx.send(f'{ctx.author.mention} **{ctx.command.name} command is on cooldown for <t:{unix}:R> **')
            await sleep(int(error.retry_after))
            await er.delete()
            return
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send('It Looks Like I Dont have permission to execute this command. Please Check My Role Position and permissions')
        elif isinstance(error, commands.errors.BadArgument):
            print(f"{ctx.author} Bad argument")
        elif isinstance(error, commands.errors.HybridCommandError):
            print('ie')
        else:
            raise (error)
