import nonebot
import time
from .data_source import everyday_url, get_pic, local_time
from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment, Message, Event

# require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

# group = ["******", "******"]
group = ["******", "******", "******"]
# scheduler.add_job()


moyu = on_command("摸鱼日历", aliases={"摸鱼", "摸了", "摸摸摸"}, rule=to_me())


@moyu.handle()
async def moyu_post(event: Event):
    moyu_url = 'https://api.j4u.ink/proxy/redirect/moyu/calendar/' + local_time(time.time()) + ".png"
    result = await get_pic(moyu_url)

    if isinstance(result, str):
        await nonebot.get_bot().send(message=result, event=event)
    else:
        await nonebot.get_bot().send(
            message=Message("摸摸摸摸摸摸~摸鱼日历来啦~\n" + (MessageSegment.image(result))),
            event=event)


everyday = on_command("60s", aliases={"今日新闻", "看世界"}, rule=to_me())


@everyday.handle()
async def daily_post(event: Event):
    result = await get_pic(everyday_url)

    if isinstance(result, str):
        await nonebot.get_bot().send(message=result, event=event)
    else:
        await nonebot.get_bot().send(message=Message("让「世界」，尽收眼底。\n" + (MessageSegment.image(result))),
                                     event=event)


async def world_daily():
    result = await get_pic(everyday_url)

    if isinstance(result, str):
        for i in group:
            await nonebot.get_bot().send_group_msg(message=result, group_id=int(i))
    else:
        for i in group:
            await nonebot.get_bot().send_group_msg(
                message=Message("让「世界」，尽收眼底。\n" + (MessageSegment.image(result))), group_id=int(i))


async def moyu_daily():
    moyu_url = 'https://api.j4u.ink/proxy/redirect/moyu/calendar/' + local_time(time.time()) + ".png"
    result = await get_pic(moyu_url)

    if isinstance(result, str):
        for i in group:
            await nonebot.get_bot().send_group_msg(message=result, group_id=int(i))
    else:
        for i in group:
            await nonebot.get_bot().send_group_msg(
                message=Message("摸摸摸摸摸摸~摸鱼日历来啦~\n" + (MessageSegment.image(result))), group_id=int(i))


scheduler.add_job(world_daily, "cron", hour=10, minute=0, id="1")
scheduler.add_job(moyu_daily, "cron", hour=8, minute=0, id="2")

logger.success("摸鱼日历启动成功！")
