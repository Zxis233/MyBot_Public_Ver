import httpx
import traceback
from nonebot.log import logger
from typing import Union
import json
import time


def local_time(timestamp) -> str:
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y%m%d", time_local)
    return dt


# 必须在__init__内手动调用
# moyu_url = 'https://api.j4u.ink/proxy/redirect/moyu/calendar/' + local_time(time.time()) + ".png"
# moyu_url = "https://api.vvhan.com/api/moyu"

everyday_url = 'https://api.vvhan.com/api/60s'


async def get_pic(url: str) -> Union[str, bytes]:
    try:
        async with httpx.AsyncClient(timeout=20) as client:  # type: ignore
            resp = await client.get(url, follow_redirects=True)
            if resp.status_code == 200:
                return resp.content
            elif resp.status_code == 429:
                return "网站访问次数达到阈值，图片无法获取，请耐心等待！"
            return f"未知错误，错误码：{resp.status_code}"

    except:
        logger.warning(traceback.format_exc())
        return "图片发送失败，请稍后再试"
