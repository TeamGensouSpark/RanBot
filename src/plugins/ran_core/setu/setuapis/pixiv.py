
import random
import re
from typing import List

from nonebot.log import logger
from ...utils import get_config
from Remilia.utils.net.pixiv import AioBypass
from pixivpy_async.sync import AppPixivAPI

pixivToken=get_config("pixivtoken",None)

def get_token():
    if pixivToken:
        return AppPixivAPI(bypass=True).login(refresh_token=pixivToken)["access_token"]
    else:
        logger.error("None Pixiv refresh_token to use")


from ..model import FinishSetuData, GetSetuConfig

class Pixiv:
    def __init__(self, config: GetSetuConfig):
        self.config = config

    async def get(self):  # p站热度榜
        accesstoken=get_token()
        if not accesstoken:
            return
        tags = self.config.tags.copy()
        if self.config.level == 1:  # R18 only
            tags.append("R-18")
        elif self.config.level == 2:  # all
            if random.choice([True, False]):
                tags.append("R-18")
        url = "https://app-api.pixiv.net/v1/search/popular-preview/illust"
        params = {
            "filter": "for_android",
            "include_translated_tag_results": "true",
            "merge_plain_keyword_results": "true",
            "word": " ".join(tags),
            "search_target": "partial_match_for_tags",
        }  # 精确:exact_match_for_tags,部分:partial_match_for_tags
        headers = pixivToken.headers()
        headers["Host"] = "app-api.pixiv.net"
        headers["Authorization"] = "Bearer {}".format(
            accesstoken
        )
        try:
            async with AioBypass.BypassClient() as client:
                res = await client.get(url, params=params, headers=headers, timeout=10)
            data = res.json()
        except Exception as e:
            logger.warning("Pixiv热度榜获取失败~:\r\n{}".format(e))
            return []
        else:
            if res.status_code == 200:
                data_finally = self.process_data(data)
                if len(data_finally) <= self.config.toGetNum - self.config.doneNum:
                    return data_finally
                else:
                    return random.sample(
                        self.process_data(data),
                        self.config.toGetNum - self.config.doneNum,
                    )
            else:
                logger.warning("Pixiv热度榜异常:{}\r\n{}".format(res.status_code, data))
                return []

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