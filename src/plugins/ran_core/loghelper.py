from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import MessageSegment,MessageEvent
import aiohttp,re,json,os
from .utils import convImg,getex_session_id
from .env import resourcePath,jdb
from Remilia.jsondb.db import JsonDB,File


if not jdb.hasTable("loghelper"):
    jdb.createTable("loghelper")
    
parselog=on_command("parselog",aliases={"分析日志"},priority=5)

@parselog.handle()
async def handle(matcher:Matcher,args:Message=CommandArg()):
    plain_text=args.extract_plain_text()
    if plain_text:
        matcher.set_arg("url",args)
        
@parselog.got("url",prompt="输入纯文本网址,例如'https://pastebin.mozilla.org/ABC23456/raw'")
async def diagnose(matcher:Matcher,event:MessageEvent,args:str=ArgPlainText("url")):
    text=await get_log(args)
    advice=await rget_advice(text,getex_session_id(event))
    if advice != None:
        await parselog.finish(convImg(advice))
    else:
        await parselog.finish("未发现已记载错误")
    
async def get_log(url):
    async with aiohttp.ClientSession() as Session:
        async with Session.get(url) as resp:
            return await resp.text()

async def rget_advice(log,session_id):
    '''
    可以考虑使用此方法替换 line:41 的方法,使用正则匹配提高准确性
    '''
    if jdb.getTable("loghelper").haskey(session_id):
        advicedict=jdb.getTable("loghelper").getkey(session_id)
    for key in advicedict.keys():
        if re.search(key,log):
            print(advicedict[key])
            return advicedict[key]
