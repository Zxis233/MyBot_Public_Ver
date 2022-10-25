from asyncio import Task
from typing import Any

from nonebot import on_command
from time import sleep
from nonebot.adapters.onebot.v11 import Event, Message
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
import asyncio
import re


def _cancel_all_tasks() -> None:
    tasks = []

    for task in asyncio.all_tasks():
        if not task.done():
            tasks.append(task)

    if not tasks:
        return

    for task in tasks:
        task_name = task.get_name()
        task_id = re.match("^Task-(\d+)", task_name).group(1)
        if int(task_id) >= 20:
            task.cancel()


the_world = on_command("砸瓦鲁多", permission=SUPERUSER, rule=to_me())


@the_world.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text
    if plain_text:
        matcher.set_arg("sleep_time", args)


@the_world.got("sleep_time")
async def _(sleep_time: str = ArgPlainText("sleep_time")):
    global time
    try:
        time = int(sleep_time)
    except:
        await the_world.finish("连「时间」都不知晓吗……")

    await the_world.send(f"「时间」，停止「{time}分钟」……")
    sleep(time * 60)
    _cancel_all_tasks()
    await the_world.finish("「时间」再度恢复流动……")
