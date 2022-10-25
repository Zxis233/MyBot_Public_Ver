from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown, CooldownIsolateLevel
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.rule import to_me
from tinydb import TinyDB, where, Query

from .config import JSON_PATH, wordbank_blacklist

db = TinyDB(
    JSON_PATH,
    encoding="utf-8",
    sort_keys=True,
    indent=4,
    ensure_ascii=False,
)

search = Query()
table = db.table("word_bank")


async def blacklist(event: GroupMessageEvent):
    return (str(event.group_id) not in wordbank_blacklist) and ("all" not in wordbank_blacklist)


word_bank = on_command("词库", rule=to_me(), priority=29)
get_message = on_message(rule=blacklist, priority=30)


@word_bank.handle()
async def _(matcher: Matcher, args: Message = CommandArg(), ):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("plain_text", args)


@word_bank.got("plain_text", prompt="想干啥？")
async def _(plain_text: str = ArgPlainText("plain_text")):
    command = plain_text.split(" ")[0]

    if len(plain_text.split(" ")) > 3:
        await word_bank.finish("参数个数过多。\n用法：\n词库 添加/删除 word1 word2")

    if command == "添加":
        first_text = plain_text.split(" ")[1]
        second_text = plain_text.split(" ")[2]
        if table.contains(where("first") == first_text):
            table.update({"second": second_text}, where("first") == first_text)
            await word_bank.finish(f"词库已更新：{first_text} {second_text}")
        else:
            table.insert({"first": first_text, "second": second_text})
            await word_bank.finish(f"词库已添加：{first_text} {second_text}")

    elif command == "删除":
        first_text = plain_text.split(" ")[1]
        second_text = plain_text.split(" ")[2]
        if table.contains(where("first") == first_text):
            table.remove(where("first") == first_text)
            await word_bank.finish(f"词库已删除：{first_text} {second_text}")
        else:
            await word_bank.finish(f"未找到关联词组！")

    elif command == "帮助":
        await word_bank.finish("用法：\n词库 添加/删除 word1 word2")

    else:
        await word_bank.finish("指令错误。")


@get_message.handle(parameterless=[Cooldown(cooldown=60, isolate_level=CooldownIsolateLevel.GROUP_USER)])
async def _(event: GroupMessageEvent):
    text: str = event.get_message().extract_plain_text()
    if table.contains(where("first") == text):
        reply = table.search(search.first == text)[0].get("second")
        await get_message.finish(reply)
