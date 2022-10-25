import re

from nonebot import on_regex, on_command, get_driver
from nonebot.adapters.onebot.v11 import MessageSegment, Message, GroupMessageEvent, Bot
from nonebot.adapters.onebot.v11.helpers import CooldownIsolateLevel, Cooldown
from nonebot.log import logger
from nonebot.params import RegexMatched
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
# from ..nonebot_plugin_getgrouplist import async_get_group_list, get_group_list
from tinydb import Query, where, TinyDB

from . import config

# group_list = get_group_list()
cqfudu_blacklist = config.cqfudu_blacklist

JSON_PATH = config.JSON_PATH

# loop = asyncio.get_event_loop()
# task = loop.create_task(async_get_group_list())
# loop.run_until_complete(task)
# loop.close()
# group_list = task.result()


driver = get_driver()

group_list = []


@driver.on_bot_connect
async def _(bot: Bot):
    global group_list
    group_list = await bot.get_group_list()
    logger.success("表情姬 获取群列表成功！")


status = Query()

db = TinyDB(
    JSON_PATH,
    encoding="utf-8",
    sort_keys=True,
    indent=4,
    ensure_ascii=False,
)
table = db.table("cq_status")

for i in group_list:
    if not table.contains(where('group_id') == i.get('group_id')):
        table.insert({"group_id": i.get('group_id'), "switch": 0})

# cqfudu_frequency = config.cqfudu_frequency
pattern = '\[CQ:face,id=(\d+)]'


async def fudu_checker(event: GroupMessageEvent) -> bool:
    return str(event.group_id) not in cqfudu_blacklist


fudu = on_regex(pattern=pattern, rule=fudu_checker)
cq_off_command = on_command("关闭表情", permission=SUPERUSER, rule=to_me())
cq_on_command = on_command("开启表情", permission=SUPERUSER, rule=to_me())


@fudu.handle(parameterless=[Cooldown(cooldown=90, isolate_level=CooldownIsolateLevel.GROUP)])
async def _(event: GroupMessageEvent, cqid=RegexMatched()):
    global bq
    group_id = event.group_id
    if table.search(status.group_id == group_id)[0].get('switch') == 1:
        grp = re.match('\[CQ:face,id=(\d+)]', str(cqid))
        if grp is not None:
            cid = grp.group(1)
            bq = MessageSegment.face(int(cid))
            await fudu.send(Message(bq))


@cq_off_command.handle()
async def control_cq(event: GroupMessageEvent):
    group_id = event.group_id

    if table.search(status.group_id == group_id)[0].get('switch') == 1:
        update_info = table.update({"switch": 0}, status.group_id == group_id)
        logger.info("已更新：" + str(update_info))
        await cq_off_command.finish("该群已关闭表情姬 ( p′︵‵。)")

    else:
        await cq_off_command.finish("不需要再关啦 >_<")


@cq_on_command.handle()
async def control_cq(event: GroupMessageEvent):
    group_id = event.group_id

    if table.search(status.group_id == group_id)[0].get('switch') == 0:
        update_info = table.update({"switch": 1}, status.group_id == group_id)
        logger.info("已更新：" + str(update_info))
        await cq_off_command.finish("该群已开启表情姬 (/≧▽≦)/~┴┴")

    else:
        await cq_off_command.finish("不需要再开啦 >_<")
