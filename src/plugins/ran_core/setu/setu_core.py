from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message,MessageSegment,MessageEvent,Bot,GroupMessageEvent
from typing import List

from .model import GetSetuConfig,FinishSetuData
from .setuapis import Yuban
from ..utils import get_config,custom_forward_msg



setuapi=get_config("setuapi","yuban")
nginxproxy=get_config("nginxproxy","i.pixiv.re")

async def Setu(event:GroupMessageEvent or MessageEvent, bot: Bot, config:GetSetuConfig):
    if config.level == 1 and isinstance(event,GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,message="变态...这种东西怎么可能在群里发给你...")
        return
    if setuapi=="yuban":
        setuall=await Yuban(config).main()
        if not setuall:
            if isinstance(event,GroupMessageEvent):
                await bot.send_group_msg(group_id=event.group_id,message="没有这种东西")
            else:
                await bot.send_private_msg(user_id=event.user_id,message="没有这种东西")
    else:
        setuall=None
    if setuall:
        setumessage=buildMessage(setuall)
        if isinstance(event,GroupMessageEvent):
            await bot.send_group_forward_msg(group_id=event.group_id,messages=custom_forward_msg(
                setumessage,
                bot.self_id
            ))
        else:
            await bot.send_private_forward_msg(user_id=event.user_id,messages=custom_forward_msg(
                setumessage,
                bot.self_id
            ))
    else:
        await bot.send(event,"错误的API配置")

def buildMessage(datalist:List[FinishSetuData]) -> List[MessageSegment]:
    return [MessageSegment.image(file=data.picLargeUrl.replace("i.pximg.net","i.pixiv.re"))+"\ntitle:%s(%s)\nauthor:%s(%s)\ntags:%s"%(data.title,data.picWebUrl,data.author,data.authorWebUrl,data.tags) for data in datalist]