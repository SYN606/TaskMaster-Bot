import discord
import asyncio
import traceback
from discord.ext import commands
from utils.config import DISCORD_TOKEN
from utils.database.prefix import get_prefix
from cogs.cogs import load_cogs  # Auto-loader
from utils.database.categories import (
    is_command_disabled, 
    is_category_disabled  # Import function to check if a category is disabled
)
from utils.config import EMOJIS


# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Bot instance
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   help_command=None)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")  # type: ignore

    # Load all cogs before starting the bot
    await load_cogs(bot)

    # Sync slash commands globally
    try:
        synced = await bot.tree.sync()
        print(f"✅ Globally synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to globally sync commands: {e}")
        traceback.print_exc()


@bot.event
async def on_message(message):
    # Ignore messages from other bots
    if message.author.bot:
        return

    # Get the prefix for the server
    prefix = await get_prefix(bot, message)

    # Check if the message is a command
    if message.content.startswith(prefix):
        command_name = message.content[len(prefix):].split()[0]  # Extract command name

        # Check if the command is disabled for the current guild
        is_disabled = await is_command_disabled(message.guild.id, command_name)

        # Get the command object
        command = bot.get_command(command_name)
        if command and command.cog:
            # Get the category (cog) the command belongs to
            cog_name = command.cog_name.lower() # type: ignore

            # Check if the category is disabled
            is_category_disabled_result = await is_category_disabled(message.guild.id, cog_name)

            if is_category_disabled_result:
                # Send an embed informing the user that the category is disabled
                embed = discord.Embed(
                    title=f"{EMOJIS['fail']} Category Disabled",
                    description=f"The category `{cog_name}` is currently disabled in this server.\n"
                                f"Commands in this category are unavailable.",
                    color=discord.Color.red()
                )
                return await message.channel.send(embed=embed)

        # If the command is disabled, prevent it from being processed
        if is_disabled:
            embed = discord.Embed(
                title=f"{EMOJIS['fail']} Command Disabled",
                description=f"The command `{command_name}` is currently disabled in this server.",
                color=discord.Color.red()
            )
            return await message.channel.send(embed=embed)

    # Check if the message mentions the bot and provide the bot's prefix and latency
    if bot.user in message.mentions:
        latency = round(bot.latency * 1000)  # Latency in ms
        embed = discord.Embed(
            title="🤖 Bot Prefix",
            description=f"My prefix here is `{prefix}`\nLatency: `{latency}ms`",
            color=discord.Color.blurple())
        await message.channel.send(embed=embed)

    # Continue processing commands
    await bot.process_commands(message)


async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)  # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
