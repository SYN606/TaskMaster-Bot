import discord
from discord.ext import commands
from utils.database.prefix import set_prefix
from utils.config import EMOJIS


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="prefix",
        description="Change the bot's command prefix (Admin only).")
    @commands.has_permissions(administrator=True)
    async def change_prefix(self,
                            ctx: commands.Context,
                            new_prefix: str = None):  # type: ignore
        """Changes the bot prefix (Admin only)."""

        # If no prefix is provided
        if new_prefix is None:
            embed = discord.Embed(
                title=f"{EMOJIS['fail']} Missing Prefix",
                description="Please provide a new prefix! Example: `!prefix ?`",
                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # If prefix length exceeds 3 characters
        if len(new_prefix) > 3:
            embed = discord.Embed(
                title=f"{EMOJIS['red_dot']} Invalid Prefix Length",
                description="Prefix cannot be longer than **3 characters**.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        # Update prefix in MongoDB
        await set_prefix(ctx.guild.id, new_prefix)  # type: ignore

        embed = discord.Embed(
            title=f"{EMOJIS['success']} Prefix Updated!",
            description=f"The bot prefix is now `{new_prefix}`",
            color=discord.Color.green())
        await ctx.send(embed=embed)

    @change_prefix.error
    async def prefix_error(self, ctx, error):
        """Handles errors for the prefix command."""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title=f"{EMOJIS['mc_emerald']} Permission Denied",
                description=
                "You **must be an Administrator** to change the prefix.",
                color=discord.Color.red())
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Prefix(bot))
