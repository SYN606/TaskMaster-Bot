import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from utils.config import EMOJIS


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="purge",
        description="Delete a number of recent messages from this channel.")
    @app_commands.describe(
        amount="Number of messages to delete (max 100)",
        member="Only delete messages from this user (optional)")
    @commands.has_permissions(manage_messages=True)
    async def purge(self,
                    ctx: commands.Context,
                    amount: int,
                    member: Optional[discord.Member] = None):
        if not ctx.guild or not isinstance(ctx.channel, discord.TextChannel):
            return await ctx.reply(
                f"{EMOJIS['fail']} This command can only be used in a server text channel.",
                ephemeral=True)

        if amount < 1 or amount > 100:
            return await ctx.reply(
                f"{EMOJIS['mc_diamond_shovel']}Please choose a number between 1 and 100.",
                ephemeral=True)

        def check(msg):
            return not member or msg.author == member

        deleted = await ctx.channel.purge(limit=amount + 1, check=check
                                          )

        embed = discord.Embed(
            description=
            f"{EMOJIS['success']} Deleted `{len(deleted)-1}` messages.",
            color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=5) # type: ignore

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(
                f"{EMOJIS['fail']} You need the **Manage Messages** permission to use this command.",
                ephemeral=True)
            
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                f"{EMOJIS['red_dot']} You need to specify how many messages to delete. Example: `--purge 10`",
                ephemeral=True)
            
        else:
            await ctx.reply(
                f"{EMOJIS['fail']} An unexpected error occurred: `{type(error).__name__}`",
                ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
