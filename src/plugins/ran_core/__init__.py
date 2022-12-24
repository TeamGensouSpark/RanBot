from nonebot import get_driver
from os import makedirs
from .env import resourcePath,cachePath,jdb
from . import (
    doujinstyle,
    utils,
    auth,
    setu,
    divination,
    loghelper,
    API,
    )

if not resourcePath.isexist:
    makedirs(resourcePath.abspath)

if not cachePath.isexist:
    makedirs(cachePath.abspath)

global_config = get_driver().config