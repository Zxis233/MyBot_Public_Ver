from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot

# config = get_driver().config.dict()
#
# nuclean_group = config.get('nuclean_group', [])

nuclean_group = ["******"]


async def checker(event: GroupMessageEvent) -> bool:
    return (event.group_id == ******) and (event.user_id == ******)


nuclean_message = on_keyword(keywords={"核酸检测通知"}, rule=checker, priority=6)


@nuclean_message.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    for i in nuclean_group:
        await bot.send_group_msg(message=event.get_message(), group_id=int(i))
