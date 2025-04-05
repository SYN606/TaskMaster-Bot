import discord
from discord.ext import commands
from utils.config import EMOJIS


class Unban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="unban",
        description="Unban a user from the server using their User ID.")
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self,
                    ctx: commands.Context,
                    user_id: int,
                    *,
                    reason: str = "No reason provided."):
        try:
            banned_users = [ban async for ban in ctx.guild.bans()] # type: ignore
            user = discord.utils.get(banned_users, user__id=user_id)

            if user is None:
                return await ctx.send(
                    f"{EMOJIS['fail']} User with ID `{user_id}` is not banned."
                )

            await ctx.guild.unban(user.user, reason=reason) # type: ignore

            embed = discord.Embed(
                title=f"{EMOJIS['success']} User Unbanned",
                description=
                f"**{user.user}** has been unbanned.\n**Reason:** {reason}",
                color=discord.Color.green())
            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send(
                f"{EMOJIS['fail']} I don't have permission to unban that user."
            )
        except discord.HTTPException as e:
            await ctx.send(f"{EMOJIS['fail']} Failed to unban user: `{e}`")
        except Exception as e:
            await ctx.send(f"{EMOJIS['fail']} Unexpected error: `{e}`")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{EMOJIS['fail']} Please provide a user ID.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{EMOJIS['fail']} Invalid user ID format.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"{EMOJIS['fail']} You don't have permission to use this command."
            )
        else:
            await ctx.send(f"{EMOJIS['fail']} Error: `{error}`")


async def setup(bot):
    await bot.add_cog(Unban(bot))
