import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Color.red()

    @commands.command()
    async def help(self, ctx, command=None):
        if not command:
            await self.send_all_commands(ctx)
        else:
            await self.send_specific_command(ctx, command)

    async def send_embed(self, ctx, title=None, description=None, color=None, url=None, timestamp=None, fields=None, thumbnail=None, image=None, author=None, footer=None, icon_url=None, proxy_icon_url=None):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )
        if url:
            embed.url = url
        if timestamp:
            embed.timestamp = timestamp

        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if image:
            embed.set_image(url=image)

        if author:
            embed.set_author(name=author, icon_url=icon_url, url=url)

        if footer:
            embed.set_footer(text=footer, icon_url=proxy_icon_url)

        await ctx.send(embed=embed)

    async def send_all_commands(self, ctx):
        embed = discord.Embed(
            title="Help", description="List of available commands (non-slash)", color=self.color)
        embed.set_thumbnail(url=self.bot.user.avatar)

        # Add Actions commands
        actions_cog = self.bot.get_cog("Actions")
        actions_commands = [
            f"`{command.name}`" for command in actions_cog.get_commands()]
        actions_command_list = " | ".join(actions_commands)
        embed.add_field(
            name="Actions", value=actions_command_list, inline=False)

        # Add Emotes commands
        emotes_cog = self.bot.get_cog("Emotes")
        emotes_commands = [
            f"`{command.name}`" for command in emotes_cog.get_commands()]
        emotes_command_list = " | ".join(emotes_commands)
        embed.add_field(name="Emotes", value=emotes_command_list, inline=False)
        util_list = ["help", "info",
                     "userinfo", "ping", "server", "invite"]
        embed.add_field(name="Utils", value=" | ".join(
            ["`{}`".format(command) for command in util_list]), inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)

        await ctx.send(embed=embed)

    async def send_specific_command(self, ctx, command):
        actions_cog = self.bot.get_cog("Actions")
        emotes_cog = self.bot.get_cog("Emotes")

        act = [i.name for i in actions_cog.get_commands()]
        if command in act:
            embed = discord.Embed()
            embed.title = 'Help ' + command
            embed.description = 'Action commands! \nShow your actions!!\n'
            embed.add_field(name='Other action commands',
                            value=','.join(act), inline=False)
            embed.color = self.color
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

        eact = [i.name for i in emotes_cog.get_commands()]
        if command in eact:
            embed = discord.Embed()
            embed.title = 'Help ' + command
            embed.description = 'Emotion commands! \nShow your emotions!!\n'
            embed.add_field(name='Other emote commands',
                            value=','.join(eact), inline=False)
            embed.color = self.color
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

        if command == 'server':
            await self.send_embed(ctx, 'Help Server', 'Shows server information', self.color, fields=[('Usage', '!server', False)], thumbnail=ctx.guild.icon, footer=f'Requested by {ctx.author}', proxy_icon_url=ctx.author.avatar)
        elif command == 'ping':
            await self.send_embed(ctx, 'Help Ping', 'Check the bot\'s latency', self.color, fields=[('Usage', '!ping', False)], thumbnail=self.bot.user.avatar, footer=f'Requested by {ctx.author}', proxy_icon_url=ctx.author.avatar)
        elif command == 'userinfo':
            await self.send_embed(ctx, 'Help Userinfo', 'Display user information', self.color, fields=[('Usage', '!userinfo [user]', False)], thumbnail=ctx.author.avatar, footer=f'Requested by {ctx.author}', proxy_icon_url=ctx.author.avatar)
        elif command == 'info':
            await self.send_embed(ctx, 'Help Info', 'Display bot information', self.color, fields=[('Usage', '!info', False)], thumbnail=self.bot.user.avatar, footer=f'Requested by {ctx.author}', proxy_icon_url=ctx.author.avatar)
        elif command == 'invite':
            await self.send_embed(ctx, 'Help Invite', 'Get the bot\'s invite link', self.color, fields=[('Usage', '!invite', False)], thumbnail=self.bot.user.avatar, footer=f'Requested by {ctx.author}', proxy_icon_url=ctx.author.avatar)
        else:
            await ctx.send(f"Command `{command}` not found.")
