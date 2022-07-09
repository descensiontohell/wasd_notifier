import asyncio

from poller.wasd_poller import poller


asyncio.run(poller.poll())
