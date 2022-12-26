import random
import re
from typing import List
from ...utils import get_config
from pixivpy_async import AppPixivAPI,PixivClient

pixivToken=get_config("pixivtoken",None)

from ..model import FinishSetuData, GetSetuConfig

class Pixiv:
    def __init__(self, config: GetSetuConfig):
        self.config = config

    async def get(self):
        tags = self.config.tags.copy()
        if self.config.level == 1:  # R18 only
            tags.append("R-18")
        elif self.config.level == 2:  # all
            if random.choice([True, False]):
                tags.append("R-18")
        async with PixivClient(bypass=True) as client:
            aapi=AppPixivAPI(client=client)
            await aapi.login(refresh_token=pixivToken)
            data=await aapi.search_illust(
                word=" ".join(tags),
                sort="popular_desc",
                filter="for_android"
                )
            data_finally = self.process_data(data)
            if len(data_finally) <= self.config.toGetNum - self.config.doneNum:
                return data_finally
            else:
                return random.sample(
                    self.process_data(data),
                    self.config.toGetNum - self.config.doneNum,
                )


    def buildOriginalUrl(self, original_url: str, page: int) -> str:
        def changePage(matched):
            if page > 1:
                return "-%s" % (int(matched[0][-1]) + 1)
            else:
                return ""

        msg_changeHost = re.sub(r"//.*/", r"//pixiv.re/", original_url)
        return re.sub(r"_p\d+", changePage, msg_changeHost)

    def process_data(self, data) -> List[FinishSetuData]:
        dataList = []
        for d in data["illusts"]:
            if d["x_restrict"] == 2:  # R18G
                continue
            if self.config.level == 0 and d["x_restrict"] == 1:  # 未开启R18
                continue
            if d["page_count"] != 1:  # 多页画廊
                OriginalUrl = d["meta_pages"][0]["image_urls"]["original"]
            else:
                OriginalUrl = d["meta_single_page"]["original_image_url"]
            dataList.append(
                FinishSetuData(
                    title=d["title"],
                    picID=d["id"],
                    picWebUrl="www.pixiv.net/artworks/" + str(d["id"]),
                    page="0",
                    author=d["user"]["name"],
                    authorID=d["user"]["id"],
                    authorWebUrl="www.pixiv.net/users/" + str(d["user"]["id"]),
                    picOriginalUrl=OriginalUrl,
                    picLargeUrl=d["image_urls"]["large"].replace("_webp", ""),
                    picMediumUrl=d["image_urls"]["medium"].replace("_webp", ""),
                    picOriginalUrl_Msg=self.buildOriginalUrl(
                        OriginalUrl, d["page_count"]
                    ),
                    tags=",".join([i["name"] for i in d["tags"]]),
                )
            )
        return dataList

    async def main(self) -> List[FinishSetuData]:
        if self.config.toGetNum - self.config.doneNum <= 0:
            return []
        if len(self.config.tags) == 0:
            return []
        return await self.get()