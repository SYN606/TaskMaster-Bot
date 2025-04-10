import discord
from discord.ext import commands
from typing import Optional
import datetime

AFK_USERS = {}  # Structure: {user_id: {"message": str, "since": datetime}}


class AFK(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="afk", description="Set your AFK status.")
    async def set_afk(self,
                      ctx: commands.Context,
                      *,
                      message: Optional[str] = "AFK"):  # type: ignore
        AFK_USERS[ctx.author.id] = {
            "message": message,
            "since": datetime.datetime.utcnow()
        }

        embed = discord.Embed(
            title="💤 AFK Enabled",
            description=f"{ctx.author.mention} You are now AFK: `{message}`",
            color=discord.Color.orange())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Remove AFK status when user sends a message
        if message.author.id in AFK_USERS:
            del AFK_USERS[message.author.id]
            embed = discord.Embed(
                title="🎉 Welcome back!",
                description="Your AFK status has been removed.",
                color=discord.Color.green())
            try:
                await message.channel.send(embed=embed, delete_after=5)
            except discord.Forbidden:
                pass

        # Notify if someone mentions an AFK user
        for user in message.mentions:
            if user.id in AFK_USERS:
                afk_data = AFK_USERS[user.id]
                since = discord.utils.format_dt(afk_data["since"], style="R")
                embed = discord.Embed(
                    title=f"💤 {user.display_name} is AFK",
                    description=
                    f"**Message:** {afk_data['message']}\n**Since:** {since}",
                    color=discord.Color.red())
                await message.channel.send(embed=embed)
                break


async def setup(bot):
    await bot.add_cog(AFK(bot))
