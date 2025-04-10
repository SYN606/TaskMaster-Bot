import discord
from discord.ext import commands
from datetime import timedelta
from utils.config import EMOJIS


class TimeoutCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def parse_duration(self, duration: str) -> timedelta | None:
        unit = duration[-1]
        try:
            value = int(duration[:-1])
        except ValueError:
            return None

        match unit:
            case "d":
                return timedelta(days=value)
            case "h":
                return timedelta(hours=value)
            case "m":
                return timedelta(minutes=value)
            case "s":
                return timedelta(seconds=value)
        return None

    @commands.hybrid_command(
        name="timeout", description="Timeout a user for a specific duration.")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.guild_only()
    async def timeout(self,
                      ctx: commands.Context,
                      member: discord.Member,
                      duration: str = "1d",
                      *,
                      reason: str = "No reason provided."):
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner: # type: ignore
            return await ctx.send(embed=discord.Embed(
                description=
                f"{EMOJIS['fail']} You can't timeout someone with an equal or higher role.",
                color=discord.Color.red()))

        delta = self.parse_duration(duration)
        if not delta:
            return await ctx.send(embed=discord.Embed(
                title=f"{EMOJIS['fail']} Invalid Time Format",
                description="Use time formats like `1d`, `2h`, `30m`, `10s`.",
                color=discord.Color.red()))

        # Attempt to DM user
        try:
            dm_embed = discord.Embed(
                title=f"{EMOJIS['announce']} You have been timed out!",
                description=
                f"You were timed out in **{ctx.guild.name}** for `{duration}`.", # type: ignore
                color=discord.Color.orange())
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            await member.send(embed=dm_embed)
        except Exception:
            pass  # DMs closed or blocked — safe to ignore

        try:
            await member.timeout(delta, reason=reason)

            embed = discord.Embed(
                title=f"{EMOJIS['success']} Timeout Issued",
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
