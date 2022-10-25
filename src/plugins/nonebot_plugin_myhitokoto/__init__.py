import httpx
import re
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from ..my_time_limiter import timelimit

yiyan = on_command("一言", aliases={"每日一句", "来一句"}, priority=3)

link = 'https://v1.hitokoto.cn/'

cd = 20

lmt = timelimit.FreqLimiter(cd)


def hitokoto_preprocessor(txt: str):
    id = re.search('"id":(\d+)', txt)
    words = re.search('"hitokoto":(.+),"ty', txt)
    author = re.search('"from_who":"(\S+)","creator":', txt)
    frm = re.search('"from":"(\S+)","fr', txt)
    tp = re.search('"type":"(\w)","fr', txt)
    tp = tp.group(1)

    if author is None:
        author = '佚名'
    else:
        author = author.group(1)

    if frm is None:
        frm = ''
    else:
        frm = frm.group(1)

    if tp == 'a':
        tp = '动画'
    elif tp == 'b':
        tp = '漫画'
    elif tp == 'c':
        tp = '游戏'
    elif tp == 'd':
        tp = '文学'
    elif tp == 'e':
        tp = '原创'
    elif tp == 'f':
        tp = '来自网络'
    elif tp == 'g':
        tp = '其他'
    elif tp == 'h':
        tp = '影视'
    elif tp == 'i':
        tp = '诗词'
    elif tp == 'j':
        tp = '网易云'
    elif tp == 'k':
        tp = '哲学'
    else:
        tp = '抖机灵'

    m = '编号：' + id.group(1) + '\t\t\t\t\t' + '类型：' + tp + '\n\n' + words.group(
        1) + '\n' + '\n\t\t\t\t\t————' + author + '《' + frm + '》'

    return m


@yiyan.handle()
async def _(event: GroupMessageEvent):
    user_id = event.user_id
    managers = ["******"]  # SUPERUSER

    if not lmt.check(user_id):
        left_time = lmt.left_time(user_id)
        await yiyan.finish(f'你刚刚叫过我啦，\n再等待{left_time:.2f}秒吧~(u‿ฺu✿)')
        return

    try:
        if not str(user_id) in managers:
            lmt.start_cd(user_id)  # 启动冷却时间限制

        async with httpx.AsyncClient() as client:  # 类似于requests的session

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/94.0.4606.81 Safari/537.36'}
            # await client.get(login)
            res = await client.get(url=link, headers=headers)
        txt = res.text

        msg = hitokoto_preprocessor(txt)
        await yiyan.finish(msg)

    except Exception as e:
        print(e)
