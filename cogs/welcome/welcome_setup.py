import discord
from discord.ext import commands
from database.welcome_db import get_welcome_config
from utils.config import EMOJIS


class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_id = member.guild.id

        config = await get_welcome_config(guild_id)
        if not config:
            return

        channel_id = config.get("channel_id")
        message_template = config.get("message")
        role_id = config.get("role_id")

        channel = member.guild.get_channel(channel_id) if channel_id else None
        if not channel or not isinstance(channel, discord.TextChannel):
            return

        welcome_message = message_template.format(
            user=member.mention,
            server=member.guild.name,
            member_count=member.guild.member_count
        ) if message_template else f"Welcome {member.mention}!"

        embed = discord.Embed(
            title=f"{EMOJIS.get('join', '👋')} Welcome to {member.guild.name}!",
            description=welcome_message,
            color=discord.Color.blurple())
        embed.set_thumbnail(url=member.display_avatar.url)

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass

        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role,
                                           reason="Auto-assigned welcome role")
                except discord.Forbidden:
                    pass


async def setup(bot):
    await bot.add_cog(Welcome(bot))
