from nonebot.adapters.onebot.v11.helpers import CooldownIsolateLevel, Cooldown
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot import on_command
from nonebot.log import logger
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Message

import linecache
import random

from pathlib import Path

group = ["******", "******", "******"]


async def checker(event: GroupMessageEvent) -> bool:
    return str(event.group_id) in group


# 获取文件行数
def getfilelines(filename, eol='\n', buffsize=4096) -> int:
    with open(filename, 'r') as handle:
        linenum = 0
        buffer = handle.read(buffsize)
        while buffer:
            linenum += buffer.count(eol)
            buffer = handle.read(buffsize)

    return linenum + 1


op_source = Path(Path.cwd(), "src/plugins/nonebot_plugin_op", "source.txt")
op_line = getfilelines(op_source)

op_msg = on_command("你说的对", rule=checker, priority=30)


@op_msg.handle(parameterless=[Cooldown(cooldown=60, isolate_level=CooldownIsolateLevel.GROUP_USER)])
async def _(bot: Bot, event: GroupMessageEvent):
    rand_line = random.randint(1, op_line)
    theline = linecache.getline(str(op_source), rand_line)
    await op_msg.finish(theline)
    # await bot.send_group_msg(message=theline, group_id=GroupMessageEvent.group_id)


add_msg = on_command("添加你说的对", rule=(checker & to_me()), priority=27, permission=SUPERUSER)


@add_msg.handle()
async def _(matcher: Matcher, args: Message = CommandArg(), ):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("plain_text", args)


@add_msg.got("plain_text")
async def _(plain_text: str = ArgPlainText("plain_text")):
    text = plain_text
    with open(op_source, 'a') as f:
        f.write("\n" + text)

    await add_msg.finish("添加语料成功！")


logger.success("你说的对，但是你说的对大全集已经加载完毕。")
