from vkbottle import Bot

from .api import api
from .blueprints import bps


def setup_bot():
    bot = Bot(api=api)
    for bp in bps:
        bp.load(bot)

    return bot


