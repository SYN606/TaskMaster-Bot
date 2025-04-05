import discord
from discord.ext import commands
from datetime import timedelta
from utils.config import EMOJIS


class TimeoutCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def parse_duration(self, duration: str):
        unit = duration[-1]
        try:
            value = int(duration[:-1])
        except ValueError:
            return None

        if unit == "d":
            return timedelta(days=value)
        elif unit == "h":
            return timedelta(hours=value)
        elif unit == "m":
            return timedelta(minutes=value)
        elif unit == "s":
            return timedelta(seconds=value)
        return None

    @commands.hybrid_command(
        name="timeout", description="Timeout a user for a specific duration.")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self,
                      ctx: commands.Context,
                      member: discord.Member,
                      duration: str = "1d",
                      *,
                      reason: str = None): # type: ignore
        try:
            delta = self.parse_duration(duration)
            if not delta:
                embed = discord.Embed(
                    title=f"{EMOJIS['fail']} Invalid Time Format",
                    description="Use formats like `1d`, `2h`, `30m`, `10s`.",
                    color=discord.Color.red())
                await ctx.send(embed=embed)
                return

            reason = reason or f"Muted for {duration}"
            await member.timeout(delta)

            embed = discord.Embed(
                title=f"{EMOJIS['success']} Timeout Successful",
                description=
                f"{member.mention} has been timed out for `{duration}`.",
                color=discord.Color.green())
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Issued by {ctx.author}",
                             icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                description=
                f"{EMOJIS['fail']} I don't have permission to timeout this user.",
                color=discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Unexpected error: `{e}`",
                color=discord.Color.red()))


async def setup(bot):
    await bot.add_cog(TimeoutCommand(bot))
