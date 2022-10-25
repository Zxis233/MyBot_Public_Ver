from pathlib import Path

from nonebot import get_driver
from nonebot.log import logger

JSON_PATH = Path(Path().cwd(), "data/word_bank.json")

config = get_driver().config.dict()

if 'wordbank_blacklist' not in config:
    logger.warning('未发现配置项 `wordbank_blacklist` , 采用默认值: ["all"]')

try:
    wordbank_blacklist = config.get("wordbank_blacklist")
except:
    logger.warning('未发现配置项 `wordbank_blacklist` , 采用默认值: ["all"]')
    wordbank_blacklist = ["all"]
