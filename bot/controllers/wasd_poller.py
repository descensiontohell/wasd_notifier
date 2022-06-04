import json
from types import SimpleNamespace
from typing import Optional

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from sqlalchemy import select, update

from bot.database.database import db
from bot.database.models import ChannelModel


class WasdController:
    def __init__(self):
        self.api_path: str = "https://wasd.tv/api/v2/broadcasts/public?channel_name={channel_name}"

    async def get_channel_data(self, channel_name: str) -> Optional[SimpleNamespace]:
        async with self.get_clientsession() as session:
            async with session.get(url=self.api_path.format(channel_name=channel_name)) as resp:
                if resp.status == 404:
                    return None

                if resp.status == 200:
                    data = await resp.text()
                    result = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
                    return result

    async def get_all_channels_names(self):
        query = select(ChannelModel.name)
        async with db.new_session() as s:
            result = await s.execute(query)
        names_list = result.scalars().all()
        return names_list

    def get_clientsession(self):
        conn = TCPConnector()
        timeout = ClientTimeout(total=10)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        }

        return ClientSession(connector=conn, headers=headers, timeout=timeout)

    async def set_state(self, channel_name: str, state: bool) -> None:
        query = update(ChannelModel).where(ChannelModel.name == channel_name).values({"state": state})
        async with db.new_session() as s:
            await s.execute(query)
            await s.commit()

    async def get_state(self, channel_name: str) -> bool:
        query = select(ChannelModel.state).where(ChannelModel.name == channel_name)
        async with db.new_session() as s:
            result = await s.execute(query)
        state = result.scalars().first()
        return state

    async def does_channel_exist(self, channel_name) -> bool:
        if await self.get_channel_data(channel_name) is not None:
            return True
        else:
            return False
