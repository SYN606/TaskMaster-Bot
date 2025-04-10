from .base_db import db


async def set_welcome_config(guild_id,
                             channel_id=None,
                             message=None,
                             role_id=None):
    update_data = {}
    if channel_id:
        update_data["welcome.channel_id"] = channel_id
    if message:
        update_data["welcome.message"] = message
    if role_id:
        update_data["welcome.role_id"] = role_id

    if update_data:
        await db.guild_configs.update_one({"guild_id": guild_id},
                                          {"$set": update_data},
                                          upsert=True)


async def get_welcome_config(guild_id):
    config = await db.guild_configs.find_one({"guild_id": guild_id})
    return config.get("welcome", {}) if config else {}
