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
    @commands.guild_only()
    async def server_banner(self, ctx: commands.Context):
        guild = ctx.guild

        if not guild.banner: # type: ignore
            embed = discord.Embed(
                title=f"{EMOJIS['fail']} No Banner Found",
                description="This server doesn't have a banner set.",
                color=discord.Color.red())
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title=f"{EMOJIS['avatar']} Server Banner - {guild.name}", # type: ignore
            color=discord.Color.blurple())
        embed.set_image(url=guild.banner.url) # type: ignore
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerBanner(bot))
