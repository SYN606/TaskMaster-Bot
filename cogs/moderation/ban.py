import discord
from discord.ext import commands
from utils.config import EMOJIS


class Ban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ban",
        description="Ban a user from the server by mention or user ID.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self,
                  ctx: commands.Context,
                  user: discord.User,
                  *,
                  reason: str = "No reason provided."):
        member = ctx.guild.get_member(user.id)  # type: ignore

        if member:
            if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:  # type: ignore
                return await ctx.send(
                    f"{EMOJIS['fail']} You can't ban someone with an equal or higher role than you."
                )

        try:
            dm_embed = discord.Embed(
                title=f"{EMOJIS['ban']} You have been banned",
                description=(
                    f"You were banned from **{ctx.guild.name}**.\n"  # type: ignore
                    f"**Reason:** {reason}"),
                color=discord.Color.red())
            dm_embed.set_footer(text=f"Issued by {ctx.author}",
                                icon_url=ctx.author.display_avatar.url)
            await user.send(embed=dm_embed)
        except discord.Forbidden:
            pass
        except Exception as e:
            await ctx.send(f"{EMOJIS['fail']} Failed to send DM: `{e}`")

        try:
            await ctx.guild.ban(  # type: ignore
                user, reason=reason, delete_message_days=0)
        except discord.Forbidden:
            return await ctx.send(
                f"{EMOJIS['fail']} I don't have permission to ban that user.")
        except Exception as e:
            return await ctx.send(
                f"{EMOJIS['fail']} Error occurred while banning: `{str(e)}`")

        embed = discord.Embed(
            title=f"{EMOJIS['success']} User Banned",
            description=(f"{EMOJIS['red_dot']} **User:** {user.mention}\n"
                         f"{EMOJIS['ping']} **Reason:** {reason}"),
            color=discord.Color.red())
        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"{EMOJIS['fail']} You don't have permission to use this command."
            )
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(f"{EMOJIS['fail']} Couldn't find that user.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{EMOJIS['fail']} You must specify a user to ban.")
        else:
            await ctx.send(f"{EMOJIS['fail']} Unexpected error: `{error}`")


async def setup(bot):
    await bot.add_cog(Ban(bot))
