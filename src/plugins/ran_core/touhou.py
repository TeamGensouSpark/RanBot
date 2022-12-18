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

thmc_site="https://doujinstyle.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

thmc=on_command("searchalbum",aliases={"搜索专辑"},rule=to_me(),priority=5)
@thmc.handle()
async def tlmchandle(event:MessageEvent,match:Matcher,args:Message=CommandArg()):
    args=args.extract_plain_text()
    if args == "":
        await thmc.finish("正确用法 '搜索专辑 搜索内容'")
    resp=await get_html(args)
    if resp != None:
        result=await format_resp(resp)
        fin=["%s. %s —— %s"%(index,resultn["name"],resultn["artist"]) for index,resultn in zip(range(1,len(result)+1),result)]
        if not os.path.exists("data/reisen/cache/%s"%event.get_session_id()):
            os.mkdir("data/reisen/cache/%s"%event.get_session_id())
        with open("data/reisen/cache/%s/tlmc.json"%event.get_session_id(),"w") as f:
            f.write(json.dumps({"result":result},indent=4))
        await thmc.send("\n".join(fin))
        await thmc.finish("使用'获取专辑 序号'来获取专辑吧")
    else:
        await thmc.finish("连接doujinstyle.com失败")

getabm=on_command("getalbum",aliases={"获取专辑"},rule=to_me(),priority=5)
@getabm.handle()
async def gabmhandle(event:MessageEvent,match:Matcher,args:Message=CommandArg()):
    if not os.path.exists("data/reisen/cache/%s/tlmc.json"%event.get_session_id()):
        await getabm.finish("缓存中暂无任何专辑,使用'获取专辑'来获取")
    else:
        with open("data/reisen/cache/%s/tlmc.json"%event.get_session_id(),"r") as f:
            resdict=json.loads(f.read())["result"]
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
    if not os.path.exists("data/reisen/cache/%s/tlmc.json"%event.get_session_id()):
        await nowabm.finish("缓存中暂无任何专辑,使用'获取专辑'来获取")
    else:
        with open("data/reisen/cache/%s/tlmc.json"%event.get_session_id(),"r") as f:
            resdict=json.loads(f.read())["result"]
        fin=["%s. %s —— %s"%(index,resultn["name"],resultn["artist"]) for index,resultn in zip(range(1,len(resdict)+1),resdict)]
        await nowabm.finish(fin)
        
async def get_html(search,page=0):
    async with aiohttp.ClientSession() as Session:
        async with Session.get("%s/?p=search&source=1&type=blanket&result=%s&page=%s"%(thmc_site,search,page),headers=headers) as resp:
            logger.info("Start to handle %s/?p=search&source=1&type=blanket&result=%s&page=%s"%(thmc_site,search,page))
            return await resp.text()


async def format_resp(html:str):
    seletor=fromstring(html)
    result=[]
    for pattern in seletor.xpath("//*[@id=\"container\"]/project/mainbar/div[3]"):
        for gridbox in pattern.xpath("//*[@class=\"gridBox\"]"):
            url=gridbox.xpath("./div[2]/a[1]/@href")[0].replace(".",thmc_site,1)
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
                "cover":thmc_site+"/thumbs"+cover
            })
    return result

async def get_redirect_url(id):
    data={"type":"1","id":id,"source":"0","download_link":""}
    async with aiohttp.ClientSession() as Session:
        async with Session.post(thmc_site,headers=headers,data=data,allow_redirects=False) as resp:
            return resp.headers.get('Location')
        
        
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
