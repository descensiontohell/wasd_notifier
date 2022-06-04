from vkbottle.bot import Blueprint, Message

from bot.const import Responses
from bot.controllers import subs, users, wasd
from bot.middlewares import AddUserMiddleware
from bot.rules.rules import SubscribeRule, UnsubscribeRule, StopRule, StartRule, SubscriptionsRule, CommandsRule

bp = Blueprint("Main flow")
bp.labeler.message_view.register_middleware(AddUserMiddleware)


@bp.on.private_message(SubscribeRule())
async def subscribe(message: Message):
    channel_name = message.text.split()[0]

    if await subs.user_is_subscribed(user_id=message.from_id, channel_name=channel_name):
        return await message.answer(Responses.ALREADY_SUBSCRIBED.format(channel_name=channel_name))

    if not await wasd.does_channel_exist(channel_name):
        return await message.answer(Responses.CHANNEL_DOES_NOT_EXIST)

    await subs.subscribe_user(user_id=message.from_id, channel_name=channel_name)
    return await message.answer(Responses.SUB_SUCCESS.format(channel_name=channel_name))


@bp.on.private_message(UnsubscribeRule())
async def unsubscribe(message: Message):
    channel_name = message.text.split()[1]

    if not await subs.user_is_subscribed(user_id=message.from_id, channel_name=channel_name):
        return await message.answer(Responses.NOT_SUBSCRIBED.format(channel_name=channel_name))

    await subs.unsubscribe_user(user_id=message.from_id, channel_name=channel_name)
    return await message.answer(Responses.UNSUB_SUCCESS.format(channel_name=channel_name))


@bp.on.private_message(StartRule())
async def start(message: Message):
    await users.user_change_status(user_id=message.from_id, is_active=True)

    await message.answer(Responses.START_SUCCESS)


@bp.on.private_message(StopRule())
async def stop(message: Message):
    await users.user_change_status(user_id=message.from_id, is_active=False)

    await message.answer(Responses.STOP_SUCCESS)


@bp.on.private_message(CommandsRule())
async def commands(message: Message):
    await message.answer(Responses.COMMANDS)


@bp.on.private_message(SubscriptionsRule())
async def subscriptions(message: Message):
    subs_list = await subs.get_user_subscriptions(user_id=message.from_id)

    await message.answer(Responses.USER_SUBS.format(subs_list="\n".join(subs_list)))


@bp.on.private_message()
async def unknown_command(message: Message):
    await message.answer(Responses.UNKNOWN_COMMAND)
