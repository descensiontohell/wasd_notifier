from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from bot.database.database import db
from bot.database.models import UserModel, ChannelModel, SubModel


class SubsController:
    async def get_channel_subscribers(self, channel_name: str) -> list[int]:
        query = select(ChannelModel).where(ChannelModel.name.ilike(channel_name)).options(selectinload(ChannelModel.subs))
        async with db.new_session() as s:
            channel = (await s.execute(query)).scalars().first()
            if channel:
                return [s.vk_id for s in channel.subs if s]
        return []

    async def get_active_channel_subscribers(self, channel_name: str) -> list[int]:
        query = select(ChannelModel, SubModel).where(and_(ChannelModel.name.ilike(channel_name), SubModel.channel_name.ilike(channel_name))).options(selectinload(ChannelModel.subs)).options(selectinload(SubModel.subs))
        async with db.new_session() as s:
            channel = (await s.execute(query)).scalars().first()
            if not channel:
                return []
            return [s.subs.vk_id for s in channel.subs if channel and s and s.subs.is_active]

    async def user_is_subscribed(self, user_id: int, channel_name: str) -> bool:
        return user_id in await self.get_channel_subscribers(channel_name=channel_name)

    async def subscribe_user(self, user_id: int, channel_name: str) -> None:
        await self.add_or_do_nothing(ChannelModel(name=channel_name))
        await self.add_or_do_nothing(SubModel(vk_id=user_id, channel_name=channel_name))

    async def unsubscribe_user(self, user_id: int, channel_name: str) -> None:
        query = select(SubModel).where(and_(SubModel.vk_id == user_id, SubModel.channel_name == channel_name))
        async with db.new_session() as s:
            subscription = (await s.execute(query)).scalars().first()
            if subscription:
                await s.delete(subscription)
                await s.commit()

    async def get_user_subscriptions(self, user_id: int) -> list[str]:
        query = select(UserModel).where(UserModel.vk_id == user_id).options(selectinload(UserModel.channels))
        async with db.new_session() as s:
            user = (await s.execute(query)).scalars().first()
            if user:
                return [s.channel_name for s in user.channels if s]
        return []

    async def add_or_do_nothing(self, *args):
        async with db.new_session() as s:
            s.add_all([*args])
            try:
                await s.commit()
            except IntegrityError:
                pass
