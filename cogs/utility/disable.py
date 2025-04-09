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
        guild_id = ctx.guild.id  # type: ignore

        # Check if the name is a command
        if self.bot.get_command(name):
            if await is_command_disabled(guild_id, name):
                return await ctx.send(
                    f"{EMOJIS['red_dot']} Command `{name}` is already disabled."
                )
            await disable_command(guild_id, name)
            return await ctx.send(f"{EMOJIS['fail']} Disabled command `{name}`"
                                  )

        # Check if the name is a valid category
        valid_categories = ["moderation", "utility", "welcome"]
        if name.lower() in valid_categories:
            if await is_category_disabled(guild_id, name.lower()):
                return await ctx.send(
                    f"{EMOJIS['red_dot']} Category `{name}` is already disabled."
                )
            await disable_category(guild_id, name.lower())
            return await ctx.send(
                f"{EMOJIS['fail']} Disabled category `{name}`")

        # If it's not a valid command or category, send an error message
        await ctx.send(
            f"{EMOJIS['red_dot']} `{name}` is not a valid command or category."
        )

    @commands.hybrid_command(
        name="enable", description="Enable a disabled command or category.")
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx: commands.Context, name: str):
        guild_id = ctx.guild.id  # type: ignore

        # Check if the name is a command
        if self.bot.get_command(name):
            if not await is_command_disabled(guild_id, name):
                return await ctx.send(
                    f"{EMOJIS['green_dot']} Command `{name}` is already enabled."
                )
            await enable_command(guild_id, name)
            return await ctx.send(
                f"{EMOJIS['success']} Enabled command `{name}`")

        # Check if the name is a valid category
        valid_categories = ["moderation", "utility", "welcome"]
        if name.lower() in valid_categories:
            if not await is_category_disabled(guild_id, name.lower()):
                return await ctx.send(
                    f"{EMOJIS['green_dot']} Category `{name}` is already enabled."
                )
            await enable_category(guild_id, name.lower())
            return await ctx.send(
                f"{EMOJIS['success']} Enabled category `{name}`")

        # If it's not a valid command or category, send an error message
        await ctx.send(
            f"{EMOJIS['red_dot']} `{name}` is not a valid command or category."
        )


# Make sure to define the setup function outside the class
async def setup(bot):
    await bot.add_cog(DisableCog(bot))
