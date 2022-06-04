from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from bot.controllers import users

checked_users = []


class AddUserMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        if self.event.from_id not in checked_users:
            await users.add_new_user(self.event.from_id)
            checked_users.append(self.event.from_id)
