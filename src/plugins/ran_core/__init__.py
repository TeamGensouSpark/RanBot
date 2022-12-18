from nonebot import get_driver
from Remilia.jsondb import db
from Remilia.lite.LiteResource import Path
from os import makedirs
from . import utils

resourcePath=Path("src/resources/ran_core/")
cachePath=Path("cache/")

if not resourcePath.isexist:
    makedirs(resourcePath.abspath)

if not cachePath.isexist:
    makedirs(cachePath.abspath)


global_config = get_driver().config

jdb=db.JsonDB(db.File(resourcePath.abspath+"/botdb.json"),dbname="bot")

