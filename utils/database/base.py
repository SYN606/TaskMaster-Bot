from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from ..config import DEFAULT_PREFIX

load_dotenv()

# MongoDB URI setup from .env
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["discord_bot"]  # Change if you want a different database name

# Collection to store each guild's configuration
guild_configs = db["guild_configs"]

# Default configuration for a new guild
default_config = {
    "prefix": DEFAULT_PREFIX,
    "disabled_commands": [],
    "disabled_categories": [],
    "logging": {
        "enabled": False,
        "channel_id": None
    },
    "welcome": {
        "enabled": False,
        "channel_id": None,
        "message": None
    },
    "afk": {},
    "custom_commands": []
}


async def init_guild(guild_id: int):
    """Initialize a new guild config if it doesn't exist."""
    existing = await guild_configs.find_one({"guild_id": guild_id})
    if not existing:
        # Insert the default config if guild is not in the database
        await guild_configs.insert_one({
            "guild_id": guild_id,
            **default_config
        })


async def get_config(guild_id: int):
    """Retrieve the current config for the given guild."""
    config = await guild_configs.find_one({"guild_id": guild_id})
    if not config:
        # Ensure the guild config is initialized if not found
        await init_guild(guild_id)
        config = await guild_configs.find_one({"guild_id": guild_id})
    return config


async def update_config(guild_id: int, updates: dict):
    """Update specific fields in the config."""
    try:
        result = await guild_configs.update_one(
            {"guild_id": guild_id}, 
            {"$set": updates},
            upsert=True  
        )
        return result.modified_count > 0  
    except Exception as e:
        print(f"Error updating config for guild {guild_id}: {e}")
        return False


# 🔁 Reset the config to default values
async def reset_config(guild_id: int):
    """Reset the guild config back to default settings."""
    try:
        result = await guild_configs.replace_one(
            {"guild_id": guild_id}, 
            {
                "guild_id": guild_id,
                **default_config
            }
        )
        return result.modified_count > 0  
    except Exception as e:
        print(f"Error resetting config for guild {guild_id}: {e}")
        return False


async def create_indexes():
    """Create necessary indexes for the guild_configs collection."""
    await guild_configs.create_index("guild_id", unique=True)


# Initialize indexes when the bot starts (this can be called in your bot setup)
async def setup_indexes():
    await create_indexes()
