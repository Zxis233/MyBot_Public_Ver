from nonebot import get_driver, logger
from pathlib import Path

config = get_driver().config.dict()

DATA_PATH = Path.cwd() / "data"
JSON_PATH = DATA_PATH / "repeater.json"

if 'repeater_group' not in config:
    logger.warning('[复读姬] 未发现配置项 `repeater_group` , 采用默认值: []')
if 'repeater_min_message_length' not in config:
    logger.warning('[复读姬] 未发现配置项 `repeater_min_message_length` , 采用默认值: 1')
if 'repeater_min_message_times' not in config:
    logger.warning('[复读姬] 未发现配置项 `repeater_min_message_times` , 采用默认值: 2')

repeater_group = config.get('repeater_group', [])
shortest_length = config.get('repeater_min_message_length', 1)
shortest_times = config.get('repeater_min_message_times', 2)
