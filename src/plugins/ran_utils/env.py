from Remilia.structdb import DataBase,YamlStruct
from Remilia.res import rPath
from nonebot import get_app,get_bot

from nonebot.adapters.onebot.v11 import Bot
from .utils import get_config


music163api=get_config("music163api",None)
realip=get_config("realip","116.25.146.177")
verify_ssl=get_config("verify_ssl",False)

app=get_app()
resourcePath=rPath(get_config("resourcePath","src/resources/ran_core/")).to_dictory().makedirs()
cachePath=rPath(get_config("cachePath","cache/")).to_dictory().makedirs()
db=DataBase(rPath(resourcePath,"botdata"),YamlStruct())

def bot() -> Bot:
    return get_bot()