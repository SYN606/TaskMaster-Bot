from discord.ext import commands
import discord
from discord import app_commands
from utils.config import EMOJIS  


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Check bot latency.")
    async def ping(self, ctx: commands.Context):
        """Check bot latency."""
        latency = round(self.bot.latency * 1000)  # Convert to ms
        embed = discord.Embed(
            title=f"{EMOJIS['pepe_ping']} Pong!",
            description=f"{EMOJIS['green_dot']} **Latency:** `{latency}ms`",
            color=discord.Color.green())
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Ping(bot))
