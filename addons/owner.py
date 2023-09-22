from discord.ext import commands


def owner():
    def predicate(ctx):
        return ctx.author.id == ctx.guild.owner.id
    return commands.check(predicate)
