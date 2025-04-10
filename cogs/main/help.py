import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional


class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="Show help for all commands or a specific one.")
    async def help(self,
                   ctx: commands.Context,
                   *,
                   command_name: Optional[str] = None):  # type: ignore
        if command_name:
            command = self.bot.get_command(command_name)
            if not command:
                return await ctx.send(f"❌ Command `{command_name}` not found.")

            embed = discord.Embed(title=f"📘 Help: `{command.qualified_name}`",
                                  description=command.description
                                  or "No description provided.",
                                  color=discord.Color.blurple())
            if command.aliases:
                embed.add_field(name="Aliases",
                                value=", ".join(command.aliases),
                                inline=False)
            embed.add_field(
                name="Usage",
                value=
                f"`{ctx.prefix}{command.qualified_name} {command.signature}`",
                inline=False)
            return await ctx.send(embed=embed)

        categories = {}

        for command in self.bot.commands:
            if command.hidden:
                continue

            module = command.callback.__module__
            parts = module.split(".")
            if len(parts) >= 2 and parts[0] == "cogs":
                category = parts[1].capitalize()
            else:
                category = "Other"

            if category not in categories:
                categories[category] = []
            categories[category].append(command)

        embed = discord.Embed(
            title="📚 Command Help",
            description=
            "Use `/help <command>` or `!help <command>` to get more info.",
            color=discord.Color.blurple())

        for category, cmds in sorted(categories.items()):
            value = ""
            for cmd in cmds:
                desc = cmd.description or "No description"
                value += f"`{cmd.name}` - {desc}\n"
            embed.add_field(name=f"📂 {category}", value=value, inline=False)

        await ctx.send(embed=embed)

    @help.autocomplete('command_name')
    async def help_autocomplete(self, interaction: discord.Interaction,
                                current: str):
        return [
            app_commands.Choice(name=cmd.name, value=cmd.name)
            for cmd in self.bot.commands
            if current.lower() in cmd.name.lower() and not cmd.hidden
        ][:25]


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
