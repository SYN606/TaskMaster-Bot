import discord
import asyncio
import traceback
from discord.ext import commands

from utils.config import DISCORD_TOKEN
from utils.database.prefix import get_prefix
from cogs.cogs import load_cogs  # Auto-loader

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
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})") # type: ignore

    await load_cogs(bot)

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

    if bot.user in message.mentions:
        prefix = await get_prefix(bot, message)
        latency = round(bot.latency * 1000)

        embed = discord.Embed(
            title="🤖 Bot Prefix",
            description=f"My prefix here is `{prefix}`\nLatency: `{latency}ms`",
            color=discord.Color.blurple())
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN) # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
