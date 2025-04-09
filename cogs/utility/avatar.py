import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from utils.config import EMOJIS


class AvatarView(discord.ui.View):

    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)
        self.member = member

    @discord.ui.button(label="Global Avatar",
                       style=discord.ButtonStyle.blurple,
                       emoji=EMOJIS["globe"])
    async def global_avatar(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        embed = discord.Embed(
            title=
            f"{EMOJIS['image']} Global Avatar - {self.member.display_name}",
            color=discord.Color.blurple())
        embed.set_image(url=self.member.avatar.url if self.member.
                        avatar else self.member.default_avatar.url)
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="Server Avatar",
                       style=discord.ButtonStyle.gray,
                       emoji=EMOJIS["server"])
    async def server_avatar(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        embed = discord.Embed(
            title=
            f"{EMOJIS['image']} Server Avatar - {self.member.display_name}",
            color=discord.Color.blurple())
        if self.member.guild_avatar:
            embed.set_image(url=self.member.guild_avatar.url)
        else:
            embed.description = f"{EMOJIS['fail']} This user has no unique server avatar."
        await interaction.response.edit_message(embed=embed, view=None)


class Avatar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="avatar",
                             description="View a user's avatar with options.",
                             aliases=["av"])
    @app_commands.describe(user="The user to view the avatar of.")
    async def avatar(self,
                     ctx: commands.Context,
                     user: Optional[discord.Member] = None):
        member = user or ctx.author

        embed = discord.Embed(
            title=
            f"{EMOJIS['info']} Choose avatar type for {member.display_name}",
            description=
            "Click a button below to view either their global or server avatar.",
            color=discord.Color.orange())
        embed.set_thumbnail(url=member.display_avatar.url)

        view = AvatarView(member) # type: ignore
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Avatar(bot))
