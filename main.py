import asyncio

from bot.bot import setup_bot
from bot.wasd_poller.poller import poller


async def main():
    bot = setup_bot()
    await poller.start()
    await bot.run_polling()


asyncio.run(main())
