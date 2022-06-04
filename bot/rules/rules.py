from vkbottle import ABCRule
from vkbottle.bot import Message

from bot.const import Commands
from bot.utils import is_valid_channel_name


class SubscribeRule(ABCRule[Message]):
    async def check(self, event: Message):
        if len(event.text.split()) == 1 and is_valid_channel_name(event.text):
            return True
        else:
            return False


class UnsubscribeRule(ABCRule[Message]):
    async def check(self, event: Message):
        text_list = event.text.split()
        if len(text_list) == 2 and text_list[0] == Commands.UNSUBSCRIBE and is_valid_channel_name(text_list[1]):
            return True
        else:
            return False


class StartRule(ABCRule[Message]):
    async def check(self, event: Message):
        return len(event.text.split()) == 1 and event.text == Commands.START


class StopRule(ABCRule[Message]):
    async def check(self, event: Message):
        return len(event.text.split()) == 1 and event.text == Commands.STOP


class CommandsRule(ABCRule[Message]):
    async def check(self, event: Message):
        return len(event.text.split()) == 1 and event.text == Commands.COMMANDS


class SubscriptionsRule(ABCRule[Message]):
    async def check(self, event: Message):
        return len(event.text.split()) == 1 and event.text == Commands.SUBSCRIPTIONS
