from commands.gamble.balance import Balance
from commands.gamble.gamble import Gamble
from commands.gamble.send import Send
from commands.gamble.daily import Daily
from commands.gamble.help import SHelp


async def setup(bot):
    await bot.add_cog(Balance(bot))
    await bot.add_cog(Gamble(bot))
    await bot.add_cog(Send(bot))
    await bot.add_cog(Daily(bot))
    await bot.add_cog(SHelp(bot))
