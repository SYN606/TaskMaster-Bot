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
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self,
                    ctx: commands.Context,
                    user_id: int,
                    *,
                    reason: str = "No reason provided."):
        try:
            banned_users = [ban
                            async for ban in ctx.guild.bans()]  # type: ignore
            user = discord.utils.get(banned_users, user__id=user_id)

            if not user:
                return await ctx.send(embed=discord.Embed(
                    description=
                    f"{EMOJIS['fail']} No banned user found with ID `{user_id}`.",
                    color=discord.Color.red()))

            await ctx.guild.unban(user.user, reason=reason)  # type: ignore

            embed = discord.Embed(
                title=f"{EMOJIS['success']} User Unbanned",
                description=
                (f"{EMOJIS['green_dot']} **User:** {user.user.mention} (`{user.user.id}`)\n"
                 f"{EMOJIS['ping']} **Reason:** {reason}"),
                color=discord.Color.green())
            embed.set_footer(text=f"Issued by {ctx.author}",
                             icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send(embed=discord.Embed(
                description=
                f"{EMOJIS['fail']} I don't have permission to unban that user.",
                color=discord.Color.red()))
        except discord.HTTPException as e:
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Failed to unban user: `{e}`",
                color=discord.Color.red()))
        except Exception as e:
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Unexpected error: `{e}`",
                color=discord.Color.red()))

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Please provide a user ID.",
                color=discord.Color.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Invalid user ID format.",
                color=discord.Color.red()))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                description=
                f"{EMOJIS['fail']} You don't have permission to use this command.",
                color=discord.Color.red()))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{EMOJIS['fail']} Error: `{error}`",
                color=discord.Color.red()))


async def setup(bot):
    await bot.add_cog(Unban(bot))
