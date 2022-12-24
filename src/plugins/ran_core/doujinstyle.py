from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import MessageSegment,MessageEvent
import aiohttp,re,json,os
from urllib.parse import quote
from lxml.html import fromstring
from .env import jdb
from .utils import getex_session_id

if not jdb.hasTable("doujinstyle"):
    jdb.createTable("doujinstyle")
    jdb.getTable("doujinstyle").setkey("cache",{}).sync()


djstyle_site="https://doujinstyle.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

djstyle=on_command("searchalbum",aliases={"搜索专辑"},rule=to_me(),priority=5)
@djstyle.handle()
async def djstylehandle(event:MessageEvent,match:Matcher,args:Message=CommandArg()):
    args=args.extract_plain_text()
    if args == "":
        await djstyle.finish("正确用法 '搜索专辑 搜索内容'")
    resp=await get_html(args)
    if resp != None:
        result=await format_resp(resp)
        if result == []:
            djstyle.finish("没有找到符合条件的专辑")
        else:
            fin=["%s. %s —— %s"%(index,resultn["name"],resultn["artist"]) for index,resultn in zip(range(1,len(result)+1),result)]
            table=jdb.getTable("doujinstyle")
            table.setAutoSync(True)
            cache=table.getkey("cache")
            cache.update({getex_session_id(event):result})
            table.setkey("cache",cache)
            await djstyle.send("\n".join(fin))
            await djstyle.finish("使用'获取专辑 序号'来获取专辑吧")
    else:
        await djstyle.finish("连接doujinstyle.com失败")

getabm=on_command("getalbum",aliases={"获取专辑"},rule=to_me(),priority=5)
@getabm.handle()
async def gabmhandle(event:MessageEvent,match:Matcher,args:Message=CommandArg()):
    cache:dict=jdb.getTable("doujinstyle").getkey("cache")
    if not cache.__contains__(getex_session_id(event)):
        await getabm.finish("缓存中暂无任何专辑,使用'获取专辑'来获取")
    else:
        resdict=cache[getex_session_id(event)]
        try:
            args=int(args.extract_plain_text())
            result=resdict[args-1]
        except:
            await getabm.finish("序号错误")
        download=await get_redirect_url(result["id"])
        fin="专辑名称：%s\n专辑作者：%s\n上传地址：%s\n下载地址：%s\n" % (result["name"],result["artist"],result["url"],quote(download).replace("%3A",":",1))
        await getabm.finish(fin+MessageSegment.image(file=result["cover"]))
        
nowabm=on_command("nowalbum",aliases={"当前专辑"},rule=to_me(),priority=5)
@nowabm.handle()
async def nabmhandle(event:MessageEvent,match:Matcher,args:Message=CommandArg()):
    cache:dict=jdb.getTable("doujinstyle").getkey("cache")
    if not cache.__contains__(getex_session_id(event)):
        await getabm.finish("缓存中暂无任何专辑,使用'获取专辑'来获取")
    else:
        resdict=cache[getex_session_id(event)]
        fin=["%s. %s —— %s"%(index,resultn["name"],resultn["artist"]) for index,resultn in zip(range(1,len(resdict)+1),resdict)]
        await nowabm.finish(fin)
        
async def get_html(search,page=0):
    async with aiohttp.ClientSession() as Session:
        async with Session.get("%s/?p=search&source=1&type=blanket&result=%s&page=%s"%(djstyle_site,search,page),headers=headers) as resp:
            logger.info("Start to handle %s/?p=search&source=1&type=blanket&result=%s&page=%s"%(djstyle_site,search,page))
            return await resp.text()


async def format_resp(html:str):
    seletor=fromstring(html)
    result=[]
    for pattern in seletor.xpath("//*[@id=\"container\"]/project/mainbar/div[3]"):
        for gridbox in pattern.xpath("//*[@class=\"gridBox\"]"):
            url=gridbox.xpath("./div[2]/a[1]/@href")[0].replace(".",djstyle_site,1)
            name=gridbox.xpath("./div[2]/a[1]/span/text()")[0]
            artist=gridbox.xpath("./div[2]/a[2]/span/text()")[0]
            identify=re.findall(r"id=\d+",url)[0].replace("id=","")
            cover=re.findall(r"/\d+.*g",gridbox.xpath("./div[1]/div/@style")[0])
            if cover == []:
                cover="/default_cover.png"
            else:
                cover=cover[0]
            result.append({
                "url":url,
                "name":name,
                "artist":artist,
                "id":identify,
                "cover":djstyle_site+"/thumbs"+cover
            })
    return result

async def get_redirect_url(id):
    data={"type":"1","id":id,"source":"0","download_link":""}
    async with aiohttp.ClientSession() as Session:
        async with Session.post(djstyle_site,headers=headers,data=data,allow_redirects=False) as resp:
            return resp.headers.get('Location')
        