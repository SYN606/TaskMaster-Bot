from .base import init_guild, get_config, update_config  # type: ignore
from utils.config import DEFAULT_PREFIX


async def get_prefix(bot, message):
    """Retrieve the prefix from the guild's config or return default."""
    if not message.guild:
        return DEFAULT_PREFIX

    guild_id = message.guild.id
    await init_guild(guild_id)  # Ensure config exists

    config = await get_config(guild_id)
    return config.get("prefix", DEFAULT_PREFIX) # type: ignore


async def set_prefix(guild_id: int, new_prefix: str):
    """Update or set the prefix in the guild's config."""
    await init_guild(guild_id)

    await update_config(guild_id, {"prefix": new_prefix})
