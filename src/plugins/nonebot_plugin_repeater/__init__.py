from nonebot import on_message, logger, on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from tinydb import TinyDB, Query, where
from . import config
import json
import re
import os

repeater_group = config.repeater_group
shortest = config.shortest_length
JSON_PATH = config.JSON_PATH

status = Query()

# db = TinyDB(JSON_PATH)


db = TinyDB(
    JSON_PATH,
    encoding="utf-8",
    sort_keys=True,
    indent=4,
    ensure_ascii=False,
)
table = db.table("repeater_status")

for i in repeater_group:
    if not table.contains(where('gid') == i):
        table.insert({"gid": i, "switch": 0})

last_message = {}
message_times = {}

m = on_message(priority=10, block=False)
repeater_off_command = on_command("关闭复读", permission=SUPERUSER, rule=to_me())
repeater_on_command = on_command("开启复读", permission=SUPERUSER, rule=to_me())


# 是否开启 打断复读 TODO
@repeater_off_command.handle()
async def control_repeater(event: GroupMessageEvent):
    gid = str(event.group_id)

    if gid in repeater_group or "all" in repeater_group:

        if table.search(status.gid == gid)[0].get('switch') == 1:
            update_info = table.update({"switch": 0}, status.gid == gid)
            logger.info("已更新：" + str(update_info))
            await repeater_off_command.finish("该群已关闭复读姬 ( p′︵‵。)")

        else:
            await repeater_off_command.finish("不需要再关啦 >_<")


@repeater_on_command.handle()
async def control_repeater(event: GroupMessageEvent):
    gid = str(event.group_id)

    if gid in repeater_group or "all" in repeater_group:

        if table.search(status.gid == gid)[0].get('switch') == 0:
            update_info = table.update({"switch": 1}, status.gid == gid)
            logger.info("已更新：" + str(update_info))
            await repeater_off_command.finish("该群已开启复读姬 (/≧▽≦)/~┴┴")

        else:
            await repeater_off_command.finish("不需要再开啦 >_<")


# 手动添加/删除群 TODO

# 消息预处理
def messagePreprocess(message: str):
    raw_message = message
    contained_images = {}
    images = re.findall(r'\[CQ:image.*?]', message)
    for i in images:
        contained_images.update({i: [re.findall(r'url=(.*?)[,\]]', i)[0][0], re.findall(r'file=(.*?)[,\]]', i)[0][0]]})
    for i in contained_images:
        message = message.replace(i, f'[{contained_images[i][1]}]')
    return message, raw_message


@m.handle()
async def repeater(bot: Bot, event: GroupMessageEvent):
    gid = str(event.group_id)
    if (gid in repeater_group or "all" in repeater_group) and (table.search(status.gid == gid)[0].get('switch') == 1):
        global last_message, message_times
        message, raw_message = messagePreprocess(str(event.message))
        logger.debug(f'这一次消息: {message}')
        logger.debug(f'上一次消息: {last_message.get(gid)}')
        if last_message.get(gid) != message:
            message_times[gid] = 1
        else:
            message_times[gid] += 1
        logger.debug(f'已重复次数: {message_times.get(gid)}/{config.shortest_times}')
        if message_times.get(gid) == config.shortest_times:
            logger.debug(f'原始的消息: {str(event.message)}')
            logger.debug(f"欲发送信息: {raw_message}")
            await bot.send_group_msg(group_id=event.group_id, message=raw_message, auto_escape=False)
        last_message[gid] = message
