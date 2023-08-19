import re
from urllib.parse import quote
import aiohttp
from lxml.html import fromstring
from nonebot.log import logger
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from RanLib.event import MessageEvent, genSessionUUID, MessageSegment
from RanLib.database import CateRanCore
from RanLib.consts import COMMON_HEADERS

find_track = on_command("find_track", rule=to_me(), aliases={"搜索专辑"}, priority=5)
get_track = on_command("get_track", rule=to_me(), aliases={"获取专辑"}, priority=5)

site = "https://doujinstyle.com"

TRACK_CACHE = CateRanCore.getTable("TRACK_CACHE")


@find_track.handle()
async def ft_handle(msge: MessageEvent, msg: Message = CommandArg()):
    args = msg.extract_plain_text()
    print(args)
    if args == "":
        await find_track.finish("正确用法 '搜索专辑 专辑名称'😅")
    resp = await searchin(args)
    if resp != None:
        result = await format_resp(resp)
        if result == []:
            await find_track.finish("没有找到符合条件的专辑😭")
        else:
            fin = [
                "%s. %s —— %s" % (index, resultn["name"], resultn["artist"])
                for index, resultn in zip(range(1, len(result) + 1), result)
            ]
            TRACK_CACHE.writeKV(genSessionUUID(msge), result)
            await find_track.send("\n".join(fin))
            await find_track.finish("使用'获取专辑 序号'来获取专辑吧😋")
    else:
        await find_track.finish("连接doujinstyle.com失败😭")


@get_track.handle()
async def gt_handle(msge: MessageEvent, msg: Message = CommandArg()):
    if not TRACK_CACHE.hasKey(genSessionUUID(msge)):
        await get_track.finish("缓存里没找到任何专辑列表😅")
    else:
        resdict = TRACK_CACHE.readValue(genSessionUUID(msge))
        try:
            index = int(msg.extract_plain_text())
            result = resdict[index - 1]
        except Exception as e:
            logger.error(e)
            await get_track.finish("序号错误")
        download = await get_redirect_url(result["id"])
        fin = "专辑名称：%s\n专辑作者：%s\n上传地址：%s\n下载地址：%s\n" % (
            result["name"],
            result["artist"],
            result["url"],
            quote(download).replace("%3A", ":", 1),
        )
        await get_track.finish(fin + MessageSegment.image(file=result["cover"]))


async def searchin(search: str, page=0):
    async with aiohttp.ClientSession() as Session:
        async with Session.get(
            "%s/?p=search&source=1&type=blanket&result=%s&page=%s"
            % (site, search, page),
            headers=COMMON_HEADERS,
        ) as resp:
            logger.info(
                "Start to handle %s/?p=search&source=1&type=blanket&result=%s&page=%s"
                % (site, search, page)
            )
            return await resp.text()


async def format_resp(html: str):
    seletor = fromstring(html)
    result = []
    for pattern in seletor.xpath('//*[@id="container"]/project/mainbar/div[3]'):
        for gridbox in pattern.xpath('//*[@class="gridBox"]'):
            url = gridbox.xpath("./div[2]/a[1]/@href")[0].replace(".", site, 1)
            name = gridbox.xpath("./div[2]/a[1]/span/text()")[0]
            artist = gridbox.xpath("./div[2]/a[2]/span/text()")[0]
            identify = re.findall(r"id=\d+", url)[0].replace("id=", "")
            cover = re.findall(r"/\d+.*g", gridbox.xpath("./div[1]/div/@style")[0])
            if cover == []:
                cover = "/default_cover.png"
            else:
                cover = cover[0]
            result.append(
                {
                    "url": str(url),
                    "name": str(name),
                    "artist": str(artist),
                    "id": str(identify),
                    "cover": "%s/thumbs%s" % (site, cover),
                }
            )
    return result


async def get_redirect_url(id):
    data = {"type": "1", "id": id, "source": "0", "download_link": ""}
    async with aiohttp.ClientSession() as Session:
        async with Session.post(
            site, headers=COMMON_HEADERS, data=data, allow_redirects=False
        ) as resp:
            return resp.headers.get("Location")
