from nonebot import get_driver
from os import makedirs
from .env import resourcePath,cachePath,jdb
from . import (
    utils,
    auth,
    setu,
    touhou,
    divination
    )

if not resourcePath.isexist:
    makedirs(resourcePath.abspath)

if not cachePath.isexist:
    makedirs(cachePath.abspath)

global_config = get_driver().config

if not jdb.hasTable("auth"):
    jdb.createTable("auth")
    table=jdb.getTable("auth")
    table.setkey("auth_session",[])
    jdb.updateTable(table)