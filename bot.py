#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter

# Custom your logger
from nonebot.log import logger, default_format

logger.add("log/error.log",
           rotation="00:00",
           diagnose=False,
           level="ERROR",
           format=default_format)

# logger.add("log/{time}.log",
#            rotation="00:00",
#            diagnose=False,
#            level="INFO",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()

app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins

# nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugin('nonebot_plugin_manager')
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin('nonebot_plugin_drawer')

nonebot.load_plugins("src/plugins")

# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
