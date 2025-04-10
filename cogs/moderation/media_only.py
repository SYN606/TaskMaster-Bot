import discord
from discord.ext import commands
from discord import app_commands
from database.base_db import get_config, update_config
from utils.config import EMOJIS


class MediaOnly(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="setmediachannel",
        description="Set a channel where only images and videos are allowed.")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_messages=True)
    @app_commands.describe(
        channel="The channel to enforce media-only rules in.")
    async def set_media_channel(self, ctx: commands.Context,
                                channel: discord.TextChannel):
        guild_id = ctx.guild.id  # type: ignore

        await update_config(guild_id, {"media_only_channel": channel.id})

        embed = discord.Embed(
            title=f"{EMOJIS['success']} Media-Only Channel Set!",
            description=
            f"Only **images** and **videos** are now allowed in {channel.mention}.",
            color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (message.author.bot or not message.guild
                or isinstance(message.channel, discord.DMChannel)):
            return

        config = await get_config(message.guild.id)
        media_channel_id = config.get("media_only_channel") if config else None

        if not media_channel_id or message.channel.id != media_channel_id:
            return

        # Allow only images or videos
        is_media = any(
            attachment.content_type and (attachment.content_type.startswith(
                "image/") or attachment.content_type.startswith("video/"))
            for attachment in message.attachments)

        if not is_media:
            try:
                await message.delete()
                warning = await message.channel.send(
                    f"{EMOJIS['fail']} Only images and videos are allowed here, {message.author.mention}!",
                    delete_after=5)
            except discord.Forbidden:
                await message.channel.send(
                    f"{EMOJIS['fail']} I don't have permission to delete messages!",
                    delete_after=5)


async def setup(bot):
    await bot.add_cog(MediaOnly(bot))
