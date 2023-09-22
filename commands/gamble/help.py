from discord import app_commands, Embed, Color, Interaction
from discord.ext import commands
from typing import List


class SHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = Color.red()

    @app_commands.command(name='help', description='Show help message for slash commands')
    @app_commands.describe(category='Select a category for info')
    @app_commands.choices(category=[
        app_commands.Choice(name="Overview", value=1),
        app_commands.Choice(name="Gamble", value=2),
        app_commands.Choice(name="Send", value=3),
        app_commands.Choice(name="Balance", value=4),
        app_commands.Choice(name="Daily", value=5)
    ])
    async def helpx(self, interaction: Interaction, category: app_commands.Choice[int]):
        if category.value == 1:
            embed = Embed(
                title="Bot Overview",
                description="Our motive is to create an engaging game bot, for which our users can without hesitation speak we love xembles",
                color=self.color
            )
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed)
        elif category.value == 2:
            embed = Embed(
                title="Gamble",
                description="Information about the gamble feature",
                color=self.color
            )
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.avatar
            )
            embed.add_field(
                name="Usage",
                value=f"/{category.name.lower()} <amount>"
            )
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed)
        elif category.value == 3:
            embed = Embed(
                title="Send",
                description="Information about the sending feature",
                color=self.color
            )
            embed.add_field(
                name="Usage",
                value=f"/{category.name.lower()} <@user> <amount [1,100000]>"
            )
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed)
        elif category.value == 4:
            embed = Embed(
                title="Balance",
                description="Shows your current holding of xembles currency",
                color=self.color
            )
            embed.add_field(
                name="Usage",
                value=f"/{category.name.lower()}"
            )
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed)
        elif category.value == 5:
            embed = Embed(
                title="Daily",
                description="Receive xembles daily",
                color=self.color
            )
            embed.add_field(
                name="Usage",
                value=f"/{category.name.lower()}"
            )
            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.set_footer(
                text=f"Requested by {interaction.user}",
                icon_url=interaction.user.avatar
            )

            await interaction.response.send_message(embed=embed)
        else:
            return
