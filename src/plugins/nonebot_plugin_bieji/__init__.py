from nonebot.adapters.onebot.v11.helpers import CooldownIsolateLevel, Cooldown
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent, Bot
from nonebot import on_command
from pathlib import Path

from nonebot import get_driver

config = get_driver().config.dict()

blacklist = config.get('bieji_blacklist', [])


async def checker(event: GroupMessageEvent) -> bool:
    return str(event.group_id) not in blacklist


bieji = on_command("bieji", aliases={"急了", "别急", "急疯了", "你先别急", "急", "很急"}, priority=2, rule=checker)
# bieji_path = Path(Path.cwd(), "src/plugins", "bieji.jpg")

bieji_path = Path(Path.cwd(), "src/plugins/nonebot_plugin_bieji", "bieji.jpg")


@bieji.handle(parameterless=[Cooldown(cooldown=60, isolate_level=CooldownIsolateLevel.GROUP)])
async def _(bot: Bot, event: GroupMessageEvent):
    await bot.send_group_msg(message=Message(MessageSegment.image(bieji_path)), group_id=event.group_id)
