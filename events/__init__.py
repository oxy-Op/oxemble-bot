from .on_ready import *
from .on_command_error import *
from .on_message import *
from .on_app_command_error import *
# from .on_guild_join import *


async def setup(bot):
    await bot.add_cog(Ready(bot))
    await bot.add_cog(Error(bot))
    await bot.add_cog(Message(bot))
    await bot.add_cog(AppError(bot))
    # await bot.add_cog(GuildJoin(bot))
