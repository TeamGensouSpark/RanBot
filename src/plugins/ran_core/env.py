from Remilia.jsondb import db
from Remilia.lite.LiteResource import Path
from nonebot import get_app,get_bot

from nonebot.adapters.onebot.v11 import Bot


app=get_app()
resourcePath=Path("src/resources/ran_core/")
cachePath=Path("cache/")
jdb=db.JsonDB(db.File(resourcePath.abspath+"/botdb.json"),dbname="bot")

def bot() -> Bot:
    return get_bot()