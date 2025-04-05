import datetime
import logging
from .base import db, init_guild
from pymongo import ASCENDING

# Logger for debugging
logger = logging.getLogger(__name__)
afk_collection = db["afk_users"]  # type: ignore


async def ensure_index():
    """Ensure indexes are set for performance."""
    try:
        await afk_collection.create_index([("user_id", ASCENDING),
                                           ("guild_id", ASCENDING)],
                                          name="user_guild_index",
                                          unique=True)
        logger.info("✅ Ensured AFK collection index.")
    except Exception as e:
        logger.error(f"❌ Failed to create index on AFK collection: {e}")


async def set_afk(user_id: int,
                  guild_id: int,
                  reason: str,
                  timestamp: datetime.datetime,
                  previous_nick: str = None): # type: ignore
    """Set a user as AFK with reason and timestamp."""
    await init_guild(guild_id)
    await ensure_index()

    try:
        await afk_collection.update_one(
            {
                "user_id": user_id,
                "guild_id": guild_id
            }, {
                "$set": {
                    "reason": reason,
                    "timestamp": timestamp,
                    "previous_nick": previous_nick or None
                }
            },
            upsert=True)
    except Exception as e:
        logger.error(f"❌ Error setting AFK for user {user_id}: {e}")


async def remove_afk(user_id: int, guild_id: int):
    """Remove AFK status and return duration + nickname."""
    try:
        afk_data = await get_afk(user_id, guild_id)
        if not afk_data:
            return None, None

        afk_duration = datetime.datetime.utcnow() - afk_data["timestamp"]
        previous_nick = afk_data.get("previous_nick")

        await afk_collection.delete_one({
            "user_id": user_id,
            "guild_id": guild_id
        })
        return afk_duration, previous_nick

    except Exception as e:
        logger.error(f"❌ Error removing AFK for user {user_id}: {e}")
        return None, None


async def get_afk(user_id: int, guild_id: int):
    """Get AFK data for a user."""
    try:
        return await afk_collection.find_one({
            "user_id": user_id,
            "guild_id": guild_id
        })
    except Exception as e:
        logger.error(f"❌ Error fetching AFK for user {user_id}: {e}")
        return None
