import discord
from discord.ext import commands
from discord import app_commands
from utils.database.afk import set_afk, remove_afk, get_afk
from utils.config import EMOJIS

from datetime import datetime, timezone


class AFK(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="afk", description="Set your AFK status with an optional reason.")
    @app_commands.describe(reason="The reason why you're AFK.")
    async def afk_command(self, ctx: commands.Context, *, reason: str = "AFK"):
        timestamp = datetime.now(timezone.utc)

        previous_nick = None
        if isinstance(ctx.author, discord.Member) and ctx.guild:
            previous_nick = ctx.author.nick or ctx.author.name
            try:
                await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
            except discord.Forbidden:
                pass  # Not enough permissions

        await set_afk(user_id=ctx.author.id,
                      guild_id=ctx.guild.id, # type: ignore
                      reason=reason,
                      timestamp=timestamp,
                      previous_nick=previous_nick or "")

        embed = discord.Embed(
            description=f"{EMOJIS['dot']} You are now marked as AFK.\n"
            f"{EMOJIS['reply']} **Reason:** {reason}",
            color=discord.Color.orange())
        await ctx.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Remove AFK if user is back
        afk_data = await get_afk(message.author.id, message.guild.id)
        if afk_data:
            afk_duration, old_nick = await remove_afk(message.author.id,
                                                      message.guild.id)

            embed = discord.Embed(
                description=
                f"{EMOJIS['heart']} Welcome back! I removed your AFK status.\n"
                f"{EMOJIS['info']} You were AFK for `{str(afk_duration).split('.')[0]}`.",
                color=discord.Color.green())

            if isinstance(message.author, discord.Member) and old_nick:
                try:
                    await message.author.edit(nick=old_nick)
                except discord.Forbidden:
                    pass

            await message.channel.send(embed=embed)

        # Notify if someone mentions an AFK user
        if message.mentions:
            for user in message.mentions:
                if user.bot:
                    continue
                afk = await get_afk(user.id, message.guild.id)
                if afk:
                    reason = afk.get("reason", "AFK")
                    timestamp = afk.get("timestamp",
                                        datetime.now(timezone.utc))
                    duration = datetime.now(timezone.utc) - timestamp

                    embed = discord.Embed(
                        description=
                        f"{EMOJIS['reply']} {user.mention} is currently AFK: **{reason}**\n"
                        f"{EMOJIS['info']} Since `{str(duration).split('.')[0]}` ago.",
                        color=discord.Color.blurple())
                    await message.channel.send(embed=embed)
                    break


async def setup(bot):
    await bot.add_cog(AFK(bot))
