from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Message
import asyncio


async def run(cmd) -> str:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'


checkin = on_command("小米签到", permission=SUPERUSER, priority=27, rule=to_me())


@checkin.handle()
async def _(matcher: Matcher, args: Message = CommandArg(), ):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("plain_text", args)


@checkin.got("plain_text", prompt="想干啥？")
async def _(plain_text: str = ArgPlainText("plain_text")):
    command = plain_text.split("  ")[0]

    if len(plain_text.split("  ")) > 3:
        await checkin.finish("参数个数过多。\n用法：\n小米签到 状态/更新 ...")

    if command == "状态":
        await checkin.finish(await run('tail -n 3 /home/zxis/qd/log.txt'))

    elif command == "更新":
        cookie = plain_text.split("  ")[1]

        with open("/home/zxis/qd/cookies.txt", "w") as f:
            f.write(cookie)
        await checkin.finish("cookie已写入！")

    elif command == "签到":
        await checkin.finish(await run('python /home/zxis/qd/miui_checkin.py'))

    else:
        await checkin.finish("指令错误。\n用法：\n小米签到 状态/更新 ...")
