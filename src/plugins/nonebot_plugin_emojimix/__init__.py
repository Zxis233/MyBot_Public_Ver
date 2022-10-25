import re
from typing import Union

import emoji

from nonebot import on_regex
from nonebot.permission import SUPERUSER
from nonebot.params import RegexDict
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent,Event
from nonebot.adapters.onebot.v11.helpers import CooldownIsolateLevel, Cooldown
from ..my_time_limiter import timelimit

from .config import Config
from .data_source import mix_emoji

cd = 60
lmt = timelimit.FreqLimiter(cd)

__plugin_meta__ = PluginMetadata(
    name="emoji合成",
    description="将两个emoji合成为一张图片",
    usage="{emoji1}+{emoji2}，如：😎+😁",
    config=Config,
    extra={
        "unique_name": "emojimix",
        "example": "😎+😁",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.1.8",
    },
)

emojis = filter(lambda e: len(e) == 1, emoji.EMOJI_DATA.keys())
pattern = "(" + "|".join(re.escape(e) for e in emojis) + ")"
emojimix = on_regex(
    rf"^\s*(?P<code1>{pattern})\s*\+\s*(?P<code2>{pattern})\s*$",
    block=True,
    priority=13,
)


@emojimix.handle()
async def _(event: GroupMessageEvent, msg: dict = RegexDict(), ):
    user_id = event.user_id
    managers = ["******"]

    if not lmt.check(user_id):
        left_time = lmt.left_time(user_id)
        await emojimix.finish(f'你刚刚叫过我啦，\n再等待{left_time:.2f}秒吧~(u‿ฺu✿)')
        return

    try:
        if not str(user_id) in managers:
            lmt.start_cd(user_id)  # 启动冷却时间限制

        emoji_code1 = msg["code1"]
        emoji_code2 = msg["code2"]
        result = await mix_emoji(emoji_code1, emoji_code2)
        if isinstance(result, str):
            await emojimix.finish(result)
        else:
            await emojimix.finish(MessageSegment.image(result))

    except Exception as e:
        print(e)
