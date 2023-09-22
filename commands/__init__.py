from .utils.info import *
from .utils.invite import *
from .utils.server import *
from .utils.userinfo import *
from .utils.ping import *
from .actions import *
from .emotes import *
from .utils.help import *
from .register import Register
from .ranking.top import Top

async def setup(bot):
    await bot.add_cog(Info(bot))
    await bot.add_cog(Invite(bot))
    await bot.add_cog(ServerInfo(bot))
    await bot.add_cog(UserInfo(bot))
    await bot.add_cog(Ping(bot))
    await bot.add_cog(Actions(bot))
    await bot.add_cog(Emotes(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Register(bot))
    await bot.add_cog(Top(bot))