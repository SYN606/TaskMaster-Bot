from .base import get_config, update_config, init_guild  # type: ignore


### ─── CATEGORY MANAGEMENT ─────────────────────────────────────
async def get_disabled_categories(guild_id: int) -> list[str]:
    """Fetch disabled categories for a guild."""
    await init_guild(guild_id)
    config = await get_config(guild_id)
    return config.get("disabled_categories", []) # type: ignore


async def disable_category(guild_id: int, category: str):
    """Disable a category for a guild."""
    await init_guild(guild_id)
    config = await get_config(guild_id)
    categories = set(config.get("disabled_categories", [])) # type: ignore
    categories.add(category.lower())

    await update_config(guild_id, {"disabled_categories": list(categories)})


async def enable_category(guild_id: int, category: str):
    """Enable a category (remove from disabled list)."""
    await init_guild(guild_id)
    config = await get_config(guild_id)
    categories = set(config.get("disabled_categories", [])) # type: ignore
    categories.discard(category.lower())

    await update_config(guild_id, {"disabled_categories": list(categories)})


async def is_category_disabled(guild_id: int, category: str) -> bool:
    """Check if a category is disabled for a guild."""
    disabled = await get_disabled_categories(guild_id)
    return category.lower() in disabled


### ─── COMMAND MANAGEMENT ──────────────────────────────────────


async def get_disabled_commands(guild_id: int) -> list[str]:
    """Fetch disabled commands for a guild."""
    await init_guild(guild_id)
    config = await get_config(guild_id)
    return config.get("disabled_commands", []) # type: ignore


async def disable_command(guild_id: int, command: str):
    """Disable a command for a guild."""
    await init_guild(guild_id)
    config = await get_config(guild_id)
    commands = set(config.get("disabled_commands", [])) # type: ignore
    commands.add(command.lower())

    await update_config(guild_id, {"disabled_commands": list(commands)})


async def enable_command(guild_id: int, command: str):
    """Enable a command (remove from disabled list)."""
    await init_guild(guild_id)
    config = await get_config(guild_id)
    commands = set(config.get("disabled_commands", [])) # type: ignore
    commands.discard(command.lower())

    await update_config(guild_id, {"disabled_commands": list(commands)})


async def is_command_disabled(guild_id: int, command: str) -> bool:
    """Check if a command is disabled for a guild."""
    disabled = await get_disabled_commands(guild_id)
    return command.lower() in disabled
