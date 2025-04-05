import discord
from discord.ext import commands
from utils.database.categories import (disable_command, enable_command,
                                       is_command_disabled, disable_category,
                                       enable_category, is_category_disabled)
from utils.config import EMOJIS


class DisableCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="disable",
        description="Disable a command or category for this server.")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx: commands.Context, name: str):
        guild_id = ctx.guild.id # type: ignore

        # Try to disable command
        if self.bot.get_command(name):
            if await is_command_disabled(guild_id, name):
                return await ctx.send(
                    f"{EMOJIS['red_dot']} Command `{name}` is already disabled."
                )
            await disable_command(guild_id, name)
            return await ctx.send(f"{EMOJIS['fail']} Disabled command `{name}`"
                                  )

        # Try to disable category
        if name.lower() in ["moderation", "utility", "welcome"]:
            if await is_category_disabled(guild_id, name.lower()):
                return await ctx.send(
                    f"{EMOJIS['red_dot']} Category `{name}` is already disabled."
                )
            await disable_category(guild_id, name.lower())
            return await ctx.send(
                f"{EMOJIS['fail']} Disabled category `{name}`")

        await ctx.send(
            f"{EMOJIS['red_dot']} `{name}` is not a valid command or category."
        )

    @commands.hybrid_command(
        name="enable", description="Enable a disabled command or category.")
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx: commands.Context, name: str):
        guild_id = ctx.guild.id # type: ignore

        # Try to enable command
        if self.bot.get_command(name):
            if not await is_command_disabled(guild_id, name):
                return await ctx.send(
                    f"{EMOJIS['green_dot']} Command `{name}` is already enabled."
                )
            await enable_command(guild_id, name)
            return await ctx.send(
                f"{EMOJIS['success']} Enabled command `{name}`")

        # Try to enable category
        if name.lower() in ["moderation", "utility", "welcome"]:
            if not await is_category_disabled(guild_id, name.lower()):
                return await ctx.send(
                    f"{EMOJIS['green_dot']} Category `{name}` is already enabled."
                )
            await enable_category(guild_id, name.lower())
            return await ctx.send(
                f"{EMOJIS['success']} Enabled category `{name}`")

        await ctx.send(
            f"{EMOJIS['red_dot']} `{name}` is not a valid command or category."
        )


async def setup(bot):
    await bot.add_cog(DisableCog(bot))
