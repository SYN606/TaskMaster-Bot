import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
DEFAULT_PREFIX = "--"

EMOJIS = {
    "mc_heart": "<:mc_heart:1357256039623295066>",
    "multiple_peeps_stare": "<:multiple_peeps_stare:1359624519677120752>",
    "avatar": "<:avatar:1359624536085102712>",
    "enjoy": "<:enjoy:1359624502811689150>",
    "announce": "<a:announce:1138564633721049098>",
    "arrow_point": "<a:arrow_point:1359629780424851567>",
    "ban": "<a:ban:1359630227445256405>",
    "boost": "<a:boost:1359631460398534796>",
    "developer": "<a:developer:1359626493713453199>",
    "fail": "<a:fail:1359630009613947011>",
    "green_dot": "<a:green_dot:1359633941245722839>",
    "okay": "<a:okay:1359630397981331707>",
    "ping": "<a:ping:1359631105333919937>",
    "red_dot": "<a:red_dot:1359633914112774406>",
    "success": "<a:success:1359630048302334145>",
    "valorant": "<a:valorant:1359630998010069062>",
    "nahi": "<:nahi:1359632467924881588>",
    "hora": "<:hora:1359632509251489984>",
    "kya": "<:kya:1359632533087584436>",
    "moderation": "<:moderation:1359630332747321585>"
}
