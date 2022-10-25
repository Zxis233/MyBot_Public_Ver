import asyncio
from time import sleep
from pathlib import Path
from typing import List, Any, Union

from nonebot import on_message, on_command, on_notice, get_driver, logger
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher import Matcher

PIC_PATH = Path(Path.cwd(), "src/plugins", "nonebot_plugin_nopoke", "poke.jpg")

SUPERUSERS: Union[list[Any], Any] = get_driver().config.dict().get('superusers', [])

from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown, CooldownIsolateLevel


async def checker(event: PokeNotifyEvent) -> bool:
    return event.is_tome() and str(event.user_id) not in SUPERUSERS


group_poke = on_notice(rule=checker, priority=9, block=False)


# @group_poke.handle([Cooldown(prompt="憋戳我 >_<", cooldown=60, isolate_level=CooldownIsolateLevel.GROUP)])
@group_poke.handle([Cooldown(cooldown=120, isolate_level=CooldownIsolateLevel.GROUP)])
async def poker(matcher: Matcher):
    msg = Message(MessageSegment.image(PIC_PATH))
    await matcher.send(message=msg)
