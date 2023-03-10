#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Remilia.lite.LiteResource import File
import os
if not os.path.exists("src/resources"):
    os.makedirs("src/resources")
    File("src/resources/additional_plugins.txt").write("w","")
addplglist=File("src/resources/additional_plugins.txt").text.splitlines()
import nonebot,os
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)
nonebot.load_plugins("src/plugins")
for _ in addplglist:
    nonebot.load_plugin(_)
#nonebot.load_from_toml("pyproject.toml")
# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...
if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
