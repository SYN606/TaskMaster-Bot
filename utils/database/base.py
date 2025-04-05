from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from ..config import DEFAULT_PREFIX

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["discord_bot"]  # Change if you want a different database name

# Collection to store each guild's config
guild_configs = db["guild_configs"]

# Default configuration for a new guild
default_config = {
    "prefix": DEFAULT_PREFIX,

    # Command and category controls
    "disabled_commands": [],
    "disabled_categories": [],

    # Logging configuration
    "logging": {
        "enabled": False,
        "channel_id": None
    },

    # Welcome system
    "welcome": {
        "enabled": False,
        "channel_id": None,
        "message": None
    },

    # AFK system (can be expanded if needed)
    "afk": {},

    # Custom commands (if any)
    "custom_commands": []
}


# 🔧 Ensure config is initialized when the bot joins a new guild
async def init_guild(guild_id: int):
    """Initialize a new guild config if it doesn't exist."""
    existing = await guild_configs.find_one({"guild_id": guild_id})
    if not existing:
        await guild_configs.insert_one({
            "guild_id": guild_id,
            **default_config
        })


# 📥 Get the current config for a guild
async def get_config(guild_id: int):
    """Retrieve the current config for the given guild."""
    return await guild_configs.find_one({"guild_id": guild_id})


# 🔄 Update specific parts of the config
async def update_config(guild_id: int, updates: dict):
    """Update specific fields in the config."""
    await guild_configs.update_one({"guild_id": guild_id}, {"$set": updates},
                                   upsert=True)


# 🔁 Reset the config to default values
async def reset_config(guild_id: int):
    """Reset the guild config back to default settings."""
    await guild_configs.replace_one({"guild_id": guild_id}, {
        "guild_id": guild_id,
        **default_config
    })
