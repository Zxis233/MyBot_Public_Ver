from nonebot import get_driver, logger
from pathlib import Path

config = get_driver().config.dict()

if 'cqfudu_blacklist' not in config:
    logger.warning('[CQ复读] 未发现配置项 `CQFUDU_BLACKLIST` , 采用默认值: []')

# if 'CQFUDU_FREQUENCY' not in config:
#     logger.warning('[CQ复读] 未发现配置项 `CQFUDU_FREQUENCY` , 采用默认值: []')

cqfudu_blacklist = config.get('cqfudu_blacklist', [])
# cqfudu_frequency = config.get('CQFUDU_FREQUENCY')

DATA_PATH = Path.cwd() / "data"
JSON_PATH = DATA_PATH / "cq.json"
