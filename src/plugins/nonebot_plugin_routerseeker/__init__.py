from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters.onebot.v11 import Event, Bot
from nonebot import get_driver, on_keyword, on_regex
import re, time

my_config = get_driver().config.dict()

router_group = my_config.get('router_group', [])


def local_time(timestamp):
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y/%m/%d %H:%M:%S", time_local)
    return dt


async def router_checker(event: GroupMessageEvent) -> bool:
    return str(event.group_id) in router_group


router_seeker = on_regex("出(.*?)路由", rule=router_checker, priority=20)


@router_seeker.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    client_id = event.get_user_id()
    msg_time = local_time(event.time)
    msg = event.get_message()
    m = f"「路由猎手」已发现「猎物」......\n时间：{msg_time}\n用户：{client_id}\n内容：{msg}"
    # await bot.send_group_msg(message=m, group_id=******)
    await bot.send_group_msg(message=m, group_id=******)


computer_seeker = on_regex("出(.*?)(主机|台式机|电脑|显卡|硬盘|内存|固态|gtx|GTX|rtx|RTX)",
                           rule=router_checker,
                           priority=20)

'''
computer_seeker = on_keyword(keywords={"主机|台式机|电脑|显卡|硬盘|内存"},
                             rule=router_checker,
                             priority=20)
'''


@computer_seeker.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    client_id = event.get_user_id()
    msg_time = local_time(event.time)
    msg = event.get_message()
    m = f"「数码猎手」已发现「猎物」......\n时间：{msg_time}\n用户：{client_id}\n内容：{msg}"
    await bot.send_group_msg(message=m, group_id=******)
