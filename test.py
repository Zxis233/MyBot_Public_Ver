import httpx
import json
import time


def local_time(timestamp) -> str:
    # 转换成localtime
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y%m%d", time_local)
    return dt


moyu_url = 'https://api.j4u.ink/proxy/redirect/moyu/calendar/' + local_time(time.time()) + ".png"

print(moyu_url)