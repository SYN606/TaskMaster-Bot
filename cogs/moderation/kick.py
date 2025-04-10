import discord
from discord.ext import commands
from utils.config import EMOJIS


class Kick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="kick",
        description="Kick a member from the server using mention or user ID.")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self,
                   ctx: commands.Context,
                   user: discord.User,
                   *,
                   reason: str = "No reason provided."):
        member = ctx.guild.get_member(user.id)  # type: ignore

        # Role hierarchy check if member exists
        if member:
            if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:  # type: ignore
                return await ctx.send(
                    f"{EMOJIS['fail']} You can't kick someone with an equal or higher role than you."
                )

        # Attempt to DM the user before kicking
        try:
            dm_embed = discord.Embed(
                title=f"{EMOJIS['announce']} You have been kicked",
                description=(f"You were kicked from **{ctx.guild.name}**.\n" # type: ignore
                             f"**Reason:** {reason}"),
                color=discord.Color.orange())
            dm_embed.set_footer(text=f"Issued by {ctx.author}",
                                icon_url=ctx.author.display_avatar.url)
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            pass  # User has DMs closed or blocked bot
        except Exception as e:
            await ctx.send(f"{EMOJIS['fail']} Couldn't send DM: `{e}`")

        # Try kicking the member (if still in guild)
        try:
            await ctx.guild.kick(user, reason=reason)  # type: ignore
        except discord.Forbidden:
            return await ctx.send(
                f"{EMOJIS['fail']} I don't have permission to kick that user.")
        except Exception as e:
            return await ctx.send(f"{EMOJIS['fail']} Error: `{str(e)}`")

        # Success embed
        embed = discord.Embed(
            title=f"{EMOJIS['success']} User Kicked",
            description=(f"{EMOJIS['red_dot']} **User:** {user.mention}\n"
                         f"{EMOJIS['ping']} **Reason:** {reason}"),
            color=discord.Color.red())
        await ctx.send(embed=embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"{EMOJIS['fail']} You don't have permission to use this command."
            )
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(f"{EMOJIS['fail']} Couldn't find that user.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"{EMOJIS['fail']} You need to mention a user or provide their ID."
            )
        else:
            await ctx.send(f"{EMOJIS['fail']} Unexpected error: `{error}`")


async def setup(bot):
    await bot.add_cog(Kick(bot))
