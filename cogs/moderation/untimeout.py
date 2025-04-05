import discord
from discord.ext import commands
from utils.config import EMOJIS


class UntimeoutCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="untimeout",
                             description="Remove timeout from a user.")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self,
                        ctx: commands.Context,
                        member: discord.Member,
                        *,
                        reason: str = "Timeout removed"):
        try:
            await member.timeout(None
                                 )  

            embed = discord.Embed(
                title=f"{EMOJIS['success']} Timeout Removed",
                description=f"{member.mention} has been un-timed out.",
                color=discord.Color.green())
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Issued by {ctx.author}",
                             icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                description=
                f"{EMOJIS['fail']} I don't have permission to untimeout this user.",
                color=discord.Color.red()))
        except discord.HTTPException as e:
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Discord API error: `{e}`",
                color=discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Unexpected error: `{e}`",
                color=discord.Color.red()))


async def setup(bot):
    await bot.add_cog(UntimeoutCommand(bot))
