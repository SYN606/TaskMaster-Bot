import discord
from discord.ext import commands
from discord import app_commands
from utils.config import EMOJIS


class ServerBanner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="serverbanner",
                             description="Get the server's banner image.",
                             aliases=["svb"])
    @app_commands.describe()
    async def server_banner(self, ctx: commands.Context):
        guild = ctx.guild

        if guild is None:
            return await ctx.send(
                f"{EMOJIS['fail']} This command can only be used in a server.")

        if guild.banner:
            embed = discord.Embed(
                title=f"{EMOJIS['image']} Server Banner - {guild.name}",
                color=discord.Color.blurple())
            embed.set_image(url=guild.banner.url)
            embed.set_footer(text=f"Requested by {ctx.author}",
                             icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                f"{EMOJIS['fail']} This server doesn't have a banner set.")


async def setup(bot):
    await bot.add_cog(ServerBanner(bot))
