import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional, Union
from utils.config import EMOJIS


class AvatarView(discord.ui.View):

    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)
        self.member = member

    @discord.ui.button(label="Global Avatar",
                       style=discord.ButtonStyle.blurple,
                       emoji=EMOJIS["okay"])
    async def global_avatar(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        await interaction.response.defer()

        url = self.member.avatar.url if self.member.avatar else self.member.default_avatar.url
        embed = discord.Embed(
            title=
            f"{EMOJIS['avatar']} Global Avatar - {self.member.display_name}",
            color=discord.Color.blurple())
        embed.set_image(url=url)
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label="Server Avatar",
                       style=discord.ButtonStyle.gray,
                       emoji=EMOJIS["multiple_peeps_stare"])
    async def server_avatar(self, interaction: discord.Interaction,
                            button: discord.ui.Button):
        await interaction.response.defer()

        embed = discord.Embed(
            title=
            f"{EMOJIS['avatar']} Server Avatar - {self.member.display_name}",
            color=discord.Color.blurple())

        if self.member.guild_avatar:
            embed.set_image(url=self.member.guild_avatar.url)
        else:
            embed.description = f"{EMOJIS['fail']} This user has no unique server avatar."

        await interaction.edit_original_response(embed=embed, view=None)


class Avatar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="avatar",
        description="View a user's avatar with global or server options.",
        aliases=["av"])
    @app_commands.describe(user="The user to view the avatar of.")
    async def avatar(self,
                     ctx: commands.Context,
                     user: Optional[Union[discord.Member,
                                          discord.User]] = None):
        target = user or ctx.author

        if isinstance(target, discord.User) and ctx.guild:
            resolved = ctx.guild.get_member(target.id)
            if resolved:
                target = resolved

        if not isinstance(target, discord.Member):
            embed = discord.Embed(
                title=f"{EMOJIS['fail']} Not a Member",
                description=
                "This user is not in this server, so I can't show their server avatar.",
                color=discord.Color.red())
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title=f"{EMOJIS['avatar']} Avatar Viewer",
            description=
            f"Click a button below to view **{target.display_name}**'s avatar.",
            color=discord.Color.orange())
        embed.set_thumbnail(url=target.display_avatar.url)

        view = AvatarView(target)
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Avatar(bot))
