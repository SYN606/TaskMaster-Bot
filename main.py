import discord
import asyncio
import traceback
from discord.ext import commands

from utils.config import DISCORD_TOKEN
from database.prefix_db import get_prefix
from cogs_laoder import load_cogs

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Bot instance
bot = commands.Bot(command_prefix=get_prefix,
                   intents=intents,
                   help_command=None)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")  # type: ignore

    # Load all cogs before syncing commands
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
    if message.author.bot:
        return

    prefix = await get_prefix(bot, message)  # type: ignore

    if bot.user in message.mentions:
        latency = round(bot.latency * 1000)
        embed = discord.Embed(
            title="🤖 Bot Prefix",
            description=f"My prefix here is `{prefix}`\nLatency: `{latency}ms`",
            color=discord.Color.blurple())
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

    for cog in bot.cogs.values():
        on_message = getattr(cog, "on_message", None)
        if callable(on_message):
            try:
                await on_message(message)  # type: ignore
            except Exception as e:
                print(f"❌ Error in {cog.__class__.__name__}.on_message: {e}")
                traceback.print_exc()


async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)  # type: ignore


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually with KeyboardInterrupt.")
    except Exception as e:
        print(f"❌ Bot stopped with error: {e}")
        traceback.print_exc()
