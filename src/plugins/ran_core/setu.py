import json,aiohttp
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import MessageSegment
#import pixivpy_async

#API=

setu=on_command("setu", rule=to_me(), aliases={"色图",}, priority=5)
#pixivpy_async.

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
LOLICONAPI="https://api.lolicon.app/setu/v2"
#@randomtouhou.handle()
#async def rthih(match:Matcher,Args:Message=CommandArg()):
#    async with aiohttp.ClientSession() as Session:
#        async with Session.get(touhouapi,headers=headers,allow_redirects=False) as resp:
#            await randomtouhou.finish(MessageSegment.image(file=resp.headers.get('Location')))

@setu.handle()
async def handle(match:Matcher,Args:Message=CommandArg()):
    tags=Args.extract_plain_text()
    async with aiohttp.ClientSession() as Session:
        async with Session.get("%s?r18=0&size=regular&tag=%s"%(LOLICONAPI,tags),headers=headers,allow_redirects=False) as resp:
            imageCon=json.loads(await resp.text())
            if imageCon["data"] != []:
                await setu.finish("标题：%s\n作者：%s\nPID：%s\n" % (imageCon["data"][0]["title"],imageCon["data"][0]["author"],imageCon["data"][0]["pid"])+MessageSegment.image(file=imageCon["data"][0]["urls"]["regular"]))
            else:
                await setu.finish("没有找到符合条件的图...")
#touhouapi="https://img.paulzzh.tech/touhou/random"
LOLICONAPI="https://api.lolicon.app/setu/v2"
from nonebot.permission import SUPERUSER
randomtouhou=on_command("randomtouhou",aliases={"随机东方",},rule=to_me(),permission=SUPERUSER)
#@randomtouhou.handle()
#async def rthih(match:Matcher,Args:Message=CommandArg()):
#    async with aiohttp.ClientSession() as Session:
#        async with Session.get(touhouapi,headers=headers,allow_redirects=False) as resp:
#            await randomtouhou.finish(MessageSegment.image(file=resp.headers.get('Location')))

@randomtouhou.handle()
async def rthihllc(match:Matcher,Args:Message=CommandArg()):
    async with aiohttp.ClientSession() as Session:
        async with Session.get("%s?r18=0&tag=東方Project|touhou|东方project&size=regular"%LOLICONAPI,headers=headers,allow_redirects=False) as resp:
            imageCon=json.loads(await resp.text())
            await randomtouhou.finish("标题：%s\n作者：%s\nPID：%s\n" % (imageCon["data"][0]["title"],imageCon["data"][0]["author"],imageCon["data"][0]["pid"])+MessageSegment.image(file=imageCon["data"][0]["urls"]["regular"]))
