import datetime
import logging
from .base import db, init_guild, get_config, update_config
from pymongo import ASCENDING

# Logger for debugging
logger = logging.getLogger(__name__)


async def ensure_index():
    """Ensure indexes are set for performance."""
    try:
        await db["guild_configs"].create_index([("guild_id", ASCENDING)],
                                               name="guild_id_index")
        logger.info("✅ Ensured guild_configs collection index.")
    except Exception as e:
        logger.error(
            f"❌ Failed to create index on guild_configs collection: {e}")


async def set_afk(user_id: int, guild_id: int, reason: str, timestamp: datetime, previous_nick: str = None): # type: ignore
    await init_guild(guild_id)
    await ensure_index()

    try:
        user_id_str = str(user_id)

        await db.guild_configs.update_one(
            {"guild_id": guild_id},
            {"$set": {
                f"afk.{user_id_str}": {
                    "reason": reason,
                    "timestamp": timestamp,
                    "previous_nick": previous_nick or None
                }
            }},
            upsert=True
        )
    except Exception as e:
        logger.error(f"❌ Error setting AFK for user {user_id}: {e}")

async def remove_afk(user_id: int, guild_id: int):
    """Remove AFK status and return duration + previous nickname."""
    try:
        # Get the guild's configuration
        guild_config = await get_config(guild_id)

        if guild_config is None or "afk" not in guild_config or user_id not in guild_config[
                "afk"]:
            return None, None

        afk_data = guild_config["afk"][user_id]
        afk_duration = datetime.datetime.utcnow() - afk_data["timestamp"]
        previous_nick = afk_data.get("previous_nick")

        del guild_config["afk"][user_id]

        await update_config(guild_id, {"afk": guild_config["afk"]})

        logger.info(f"✅ User {user_id} removed from AFK in guild {guild_id}.")
        return afk_duration, previous_nick

    except Exception as e:
        logger.error(
            f"❌ Error removing AFK for user {user_id} in guild {guild_id}: {e}"
        )
        return None, None


async def get_afk(user_id: int, guild_id: int):
    """Get AFK data for a user."""
    try:
        guild_config = await get_config(guild_id)

        if guild_config is None or "afk" not in guild_config or user_id not in guild_config[
                "afk"]:
            return None

        return guild_config["afk"][user_id]
    except Exception as e:
        logger.error(
            f"❌ Error fetching AFK for user {user_id} in guild {guild_id}: {e}"
        )
        return None


async def check_if_afk(user_id: int, guild_id: int):
    """Check if a user is currently AFK in the given guild."""
    afk_data = await get_afk(user_id, guild_id)
    if afk_data:
        return True
    return False
