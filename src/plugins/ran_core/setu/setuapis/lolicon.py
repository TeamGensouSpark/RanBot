import aiohttp
from typing import List
from nonebot.log import logger

from ..model import FinishSetuData, GetSetuConfig
from ...utils import get_config
nginxproxy=get_config("nginxproxy","i.pixiv.re")

class Lolicon:
    def __init__(self, config: GetSetuConfig):
        self.config = config

    async def get(self) -> List[FinishSetuData]:
        try:
            # with httpx.Client() as client:
            async with aiohttp.ClientSession() as Session:
                async with Session.post(
                    url="https://api.lolicon.app/setu/v2",
                    json={
                        "r18": self.config.level,
                        "num": self.config.toGetNum - self.config.doneNum,
                        "tag": self.config.tags,
                        "size": ["original", "regular", "small"],
                        "proxy": False,
                    },
                    timeout=8,
                ) as resp:
                    resjson=await resp.json()
                    res_code=resp.status
        except Exception as e:
            logger.warning("Lolicon:\r\n{}".format(e))
            return []
        if res_code == 200:
            dataList = []
            datas = resjson["data"]
            for d in datas:
                dataList.append(
                    FinishSetuData(
                        title=d["title"],
                        picID=d["pid"],
                        picWebUrl="www.pixiv.net/artworks/" + str(d["pid"]),
                        page=d["p"],
                        author=d["author"],
                        authorID=d["uid"],
                        authorWebUrl="www.pixiv.net/users/" + str(d["uid"]),
                        picOriginalUrl=d["urls"]["original"],
                        picLargeUrl=d["urls"]["regular"],
                        picMediumUrl=d["urls"]["small"],
                        picOriginalUrl_Msg=d["urls"]["original"].replace(
                            "i.pximg.net", nginxproxy
                        ),
                        # tags=self.config.tags,
                        tags=",".join(d["tags"]),
                    )
                )
            return dataList
        return []

    async def main(self) -> List[FinishSetuData]:
        if self.config.toGetNum - self.config.doneNum <= 0:
            return []
        return await self.get()