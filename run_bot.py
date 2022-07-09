import asyncio

from bot.bot import setup_bot


async def main():
    bot = setup_bot()
    await bot.run_polling()


asyncio.run(main())
