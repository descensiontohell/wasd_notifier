from vkbottle import Bot

from bot_token import BOT_TOKEN
from .blueprints import bps


def setup_bot():
    bot = Bot(BOT_TOKEN)
    for bp in bps:
        bp.load(bot)

    return bot


