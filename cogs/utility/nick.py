import discord
from discord.ext import commands
from typing import Optional, Union
from utils.config import EMOJIS


class Nickname(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="nick",
                             aliases=["nickname", "setnick"],
                             description="Change or reset a user's nickname.")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.guild_only()
    async def nick(self,
                   ctx: commands.Context,
                   user: Optional[Union[discord.Member, discord.User]] = None,
                   *,
                   nickname: Optional[str] = None):
        user = user or ctx.author

        # Convert to Member if it's just a User
        member: Optional[discord.Member] = None
        if isinstance(user, discord.User):
            member = ctx.guild.get_member(user.id) if ctx.guild else None
        elif isinstance(user, discord.Member):
            member = user

        if not member:
            return await ctx.send(embed=discord.Embed(
                title=f"{EMOJIS['fail']} Member Not Found",
                description="I couldn't find that user in this server.",
                color=discord.Color.red()))

        # Check if bot can act on the member
        if not ctx.guild.me or not ctx.guild.me.guild_permissions.manage_nicknames: # type: ignore
            return await ctx.send(embed=discord.Embed(
                title=f"{EMOJIS['fail']} Missing Permissions",
                description=
                "I need the **Manage Nicknames** permission to do that.",
                color=discord.Color.red()))

        # Check hierarchy
        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role: # type: ignore
            return await ctx.send(embed=discord.Embed(
                title=f"{EMOJIS['fail']} Role Hierarchy",
                description=
                "You can't change the nickname of someone with an equal or higher role than you.",
                color=discord.Color.red()))

        try:
            await member.edit(nick=nickname)
        except discord.Forbidden:
            return await ctx.send(embed=discord.Embed(
                title=f"{EMOJIS['fail']} Action Forbidden",
                description=
                "I can't change that nickname due to Discord's role hierarchy.",
                color=discord.Color.red()))
        except Exception as e:
            return await ctx.send(
                embed=discord.Embed(title=f"{EMOJIS['fail']} Error",
                                    description=f"Something went wrong: `{e}`",
                                    color=discord.Color.red()))

        # Success message
        if nickname:
            embed = discord.Embed(
                title=f"{EMOJIS['success']} Nickname Updated",
                description=
                f"{member.mention}'s nickname has been set to **{nickname}**.",
                color=discord.Color.green())
        else:
            embed = discord.Embed(
                title=f"{EMOJIS['success']} Nickname Reset",
                description=
                f"{member.mention}'s nickname has been reset to their default name.",
                color=discord.Color.green())

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Nickname(bot))
