from os import makedirs
from Remilia.jsondb import db
from Remilia.lite.LiteResource import Path
from nonebot import get_app,get_bot,get_driver

from nonebot.adapters.onebot.v11 import Bot
from .utils import get_config


music163api=get_config("music163api",None)
realip=get_config("realip","116.25.146.177")
verify_ssl=get_config("verify_ssl",False)

app=get_app()
resourcePath=Path(get_config("resourcePath","src/resources/ran_core/"))
cachePath=Path(get_config("cachePath","cache/"))
if not resourcePath.isexist:
    makedirs(resourcePath.abspath)
if not cachePath.isexist:
    makedirs(cachePath.abspath)
jdb=db.JsonDB(db.File(resourcePath.abspath+"/botdb.json"),dbname="bot")

def bot() -> Bot:
    return get_bot()