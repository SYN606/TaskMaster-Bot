import os
import traceback


async def load_cogs(bot):
    base_path = os.path.join(os.path.dirname(__file__), "cogs")
    base_package = "cogs"

    for category in os.listdir(base_path):
        category_path = os.path.join(base_path, category)

        if not os.path.isdir(category_path) or category.startswith("__"):
            continue

        for file in os.listdir(category_path):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]
                ext_path = f"{base_package}.{category}.{module_name}"

                try:
                    await bot.load_extension(ext_path)
                    print(f"✅ Loaded: {ext_path}")
                except Exception as e:
                    print(
                        f"❌ Failed to load {ext_path}: {type(e).__name__}: {e}"
                    )
                    traceback.print_exc()
