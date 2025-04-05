import discord
from discord.ext import commands
from utils.config import EMOJIS


class DynamicHelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="Shows all available commands grouped by category.")
    async def help_command(self, ctx: commands.Context):
        await ctx.defer()  

        embed = discord.Embed(
            title=f"{EMOJIS['heart']} Help Menu",
            description=
            f"{EMOJIS['dot']} Here are all my commands grouped by category:",
            color=discord.Color.blurple())
        categories = {}

        for command in self.bot.commands:
            if command.hidden:
                continue

            cog_name = command.cog_name or "Uncategorized"
            categories.setdefault(cog_name, []).append(command)

        for category, commands_list in categories.items():
            command_list = ""
            for cmd in commands_list:
                desc = cmd.description or cmd.help or f"{EMOJIS['warn']} No description"
                command_list += f"• `{cmd.name}` — {desc}\n"

            embed.add_field(name=f"{EMOJIS['reply']} {category}",
                            value=command_list,
                            inline=False)

        embed.set_footer(
            text=
            f"{EMOJIS['info']} Use '{ctx.prefix}<command>' for more details.")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(DynamicHelpCommand(bot))
