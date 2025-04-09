import os


async def load_cogs(bot):
    base_dir = os.path.dirname(__file__)
    package_name = __package__ or 'cogs'

    # 🔹 Load nested cogs (e.g., cogs/utility/afk.py)
    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)
        if os.path.isdir(category_path) and not category.startswith('__'):
            for file in os.listdir(category_path):
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = file[:-3]
                    ext_path = f'{package_name}.{category}.{module_name}'
                    await _try_load_extension(bot, ext_path)

    # 🔹 Load top-level cogs (e.g., cogs/help.py)
    for file in os.listdir(base_dir):
        if (file.endswith('.py') and not file.startswith('__')
                and file != "cogs.py"):
            module_name = file[:-3]
            ext_path = f"{package_name}.{module_name}"
            await _try_load_extension(bot, ext_path)


async def _try_load_extension(bot, ext_path):
    try:
        await bot.load_extension(ext_path)
        print(f"✅ Loaded: {ext_path}")
    except Exception as e:
        print(f"❌ Failed to load {ext_path}: {type(e).__name__}: {e}")
