from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.log import logger
import aiohttp
from json import loads
from ..ran_utils.env import music163api,realip,verify_ssl

conn=aiohttp.TCPConnector(verify_ssl=verify_ssl)
picksong=on_command("picksong",aliases={"点歌"},rule=to_me(),priority=5)
#https://binaryify.github.io/NeteaseCloudMusicApi/#/?id=vercel-%e9%83%a8%e7%bd%b2
#使用前先在.env.xxx中设置网易云API👆
@picksong.handle()
async def handle(matcher:Matcher,args:Message=CommandArg()):
    if music163api:
        plain_text=args.extract_plain_text()
        if plain_text:
            matcher.set_arg("kw",args)
    else:
        await picksong.finish("请先在.env中配置网易云API（MUSIC163API=\"xxxxx\"），可参考https://binaryify.github.io/NeteaseCloudMusicApi/#/?id=vercel-%e9%83%a8%e7%bd%b2")

@picksong.got("kw","输入搜索歌名")
async def got(args:str=ArgPlainText("kw")):
    searchdict=loads(await get_searchtext(args))
    if not searchdict["result"].__contains__("songs"):
        await picksong.finish("未找到相关歌曲")
    resongid=searchdict["result"]["songs"][0]["id"]
    songdict=loads(await get_songdetail(resongid))
    resongdt=songdict["songs"][0]
    await picksong.finish(MessageSegment(
        "music",{
            "type": "custom",
            "subtype": "163",
            "url": "https://music.163.com/#/song?id=%s"%resongid,
            "audio": "http://music.163.com/song/media/outer/url?id=%s"%resongid,
            "title": "%s"%resongdt["name"],
            "content": resongdt["ar"][0]["name"],
            "image": resongdt["al"]["picUrl"],
            },
        )
    )

async def get_songdetail(ids:str):
    logger.info("with id %s"%ids)
    postjson={
        "realIP":realip,
        "ids":str(ids)
    }
    async with aiohttp.request('POST',"%s/song/detail"%music163api, connector=conn,json=postjson) as resp:
        return await resp.text()

async def get_searchtext(kw:str) -> str:
    logger.info("start search with kw %s"%kw)
    postjson={
        "realIP":realip,
        "keywords":kw
    }
    async with aiohttp.request('POST',"%s/search"%music163api, connector=conn,json=postjson) as resp:
        return await resp.text()