from discord import Embed, Color, ButtonStyle, Interaction
from discord.ui import View, Button
from discord.ext import commands
from database.manage import Database
from asyncio import TimeoutError


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
        self.view = View()

    @commands.hybrid_command(name='register', with_app_command=True, description='Register yourself with us')
    async def _register(self, ctx: commands.Context):
        if not self.db.check_user_existence(ctx.author.id):
            embed = Embed(
                title='Register',
                description='By confirming, you are accepting our privacy policy.',
                color=Color.blue()
            )
            embed.set_thumbnail(url=ctx.author.avatar)
            embed.set_footer(text=str(ctx.author),
                             icon_url=ctx.author.avatar)
            button = Button(
                label='Confirm', style=ButtonStyle.primary, custom_id='register')

            async def btn_callback(i: Interaction):
                if i.user == ctx.author:
                    await i.response.send_message('Confirmed')
                    self.db.create_user(ctx.author.id)
                    self.view.clear_items()
                    await r.edit(view=None)

            button.callback = btn_callback

            self.view.add_item(button)
            r = await ctx.send(embed=embed, view=self.view)
            try:
                interaction = await self.bot.wait_for(
                    "button_click",
                    check=lambda i: i.component.label == "Confirm",
                    timeout=30.0
                )
                if interaction:
                    print('yes')
            except TimeoutError:
                await r.edit(content='Timeout registration', view=None)
        else:
            await ctx.send("You are already registered")