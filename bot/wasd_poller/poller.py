import asyncio
import logging
from asyncio import Task
from random import randint
from typing import Optional

from bot.api import api
from bot.const import Responses
from bot.controllers import wasd, subs


class WasdPoller:
    def __init__(self):
        self.is_running: bool = False
        self.poll_task: Optional[Task] = None
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("Poller")

    async def start(self):
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            list_of_channel_names = await wasd.get_all_channels_names()

            for channel_name in list_of_channel_names:
                await asyncio.sleep(1)

                channel_info = await wasd.get_channel_data(channel_name=channel_name)
                self.logger.info(channel_info)
                try:
                    stream_title = channel_info.result.media_container.media_container_name
                    stream_game = channel_info.result.media_container.game.game_name
                    name = channel_info.result.channel.channel_name
                except AttributeError:
                    await wasd.set_state(channel_name, False)
                    continue

                state = await wasd.get_state(channel_name)
                self.logger.info(msg=f"{channel_name} {channel_info.result.channel.channel_is_live} {state}")
                if channel_info.result.channel.channel_is_live is True and state is False:
                    await self.notify_users(name, stream_title, stream_game)
                    await wasd.set_state(channel_name, True)

            await asyncio.sleep(5)

    async def notify_users(self, channel_name: str, stream_title: str, stream_game: str) -> None:
        notified_users = await subs.get_active_channel_subscribers(channel_name=channel_name)
        for user_id in notified_users:
            await api.messages.send(
                peer_id=user_id,
                random_id=randint(0, 100),
                message=Responses.STREAM_STARTED.format(
                    channel=channel_name,
                    stream_title=stream_title,
                    stream_game=stream_game,
                    link_name=channel_name.lower(),
                )
            )


poller = WasdPoller()
