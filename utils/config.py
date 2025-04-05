import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
DEFAULT_PREFIX = "--"

EMOJIS = {
    "fail": "<:fail:1357256726088515767>",
    "mc_diamond": "<:mc_diamond:1357255945650180219>",
    "mc_diamond_shovel": "<:mc_diamond_shovel:1357256027665465354>",
    "mc_emerald": "<:mc_emerald:1357256031696191618>",
    "mc_heart": "<:mc_heart:1357256039623295066>",
    "success": "<:success:1357256962798256248>",
    "pepe_ping": "<:pepe_ping:1357983973380198565>",
    "red_dot": "<:red_dot:1357983970234466345>",
    "green_dot": "<:green_dot:1357983967042605129>"
}
