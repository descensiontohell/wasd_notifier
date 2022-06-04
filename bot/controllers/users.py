from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from bot.database.database import db
from bot.database.models import UserModel


class UsersController:
    async def add_new_user(self, user_id: int) -> None:
        async with db.new_session() as s:
            s.add_all([UserModel(vk_id=user_id)])
            try:
                await s.commit()
            except IntegrityError:
                pass

    async def user_change_status(self, user_id: int, is_active: bool) -> None:
        query = update(UserModel).where(UserModel.vk_id == user_id).values({"is_active": is_active})
        async with db.new_session() as s:
            await s.execute(query)
            await s.commit()

