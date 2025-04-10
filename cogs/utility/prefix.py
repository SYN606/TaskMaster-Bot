import discord
from discord.ext import commands
from database.prefix_db import set_prefix
from utils.config import EMOJIS


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="prefix",
        description="Change the bot's command prefix (Admin only).")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def change_prefix(self,
                            ctx: commands.Context,
                            new_prefix: str = None):  # type: ignore
        if new_prefix is None:
            embed = discord.Embed(
                title=f"{EMOJIS['fail']} Missing Prefix",
                description="Please provide a new prefix! Example: `!prefix ?`",
                color=discord.Color.red())
            return await ctx.send(embed=embed)

        if len(new_prefix) > 3:
            embed = discord.Embed(
                title=f"{EMOJIS['red_dot']} Invalid Prefix Length",
                description="Prefix cannot be longer than **3 characters**.",
                color=discord.Color.red())
            return await ctx.send(embed=embed)

        await set_prefix(ctx.guild.id, new_prefix)  # type: ignore

        embed = discord.Embed(
            title=f"{EMOJIS['success']} Prefix Updated!",
            description=f"The bot prefix is now `{new_prefix}`",
            color=discord.Color.green())
        await ctx.send(embed=embed)

    @change_prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title=f"{EMOJIS['fail']} Permission Denied",
                description=
                "You **must be an Administrator** to change the prefix.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{EMOJIS['fail']} Unexpected Error",
                description=f"`{type(error).__name__}`: {error}",
                color=discord.Color.red())
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Prefix(bot))
