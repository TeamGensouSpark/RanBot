import re
from nonebot import on_regex
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment,GroupMessageEvent
from nonebot.log import logger
from nonebot.params import StateParam
from nonebot.typing import T_State

from .model import GetSetuConfig
from .setu_core import Setu



digitalConversionDict = {
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}
callsetu = on_regex('来(.*?)[点丶、个份张幅](.*?)的?([rR]18)?[色瑟涩䔼😍🐍][图圖🤮]', priority=5,rule=to_me())

@callsetu.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State = StateParam()):
    config_getSetu: GetSetuConfig = GetSetuConfig()
    info = state["_matched_groups"]
    if info[0] != "":
        if info[0] in digitalConversionDict.keys():
            config_getSetu.toGetNum = int(digitalConversionDict[info[0]])
        else:
            if info[0].isdigit():
                config_getSetu.toGetNum = int(info[0])
            else:
                await callsetu.send(MessageSegment.text('能不能用阿拉伯数字?'))
                logger.info('非数字')
                return None
    else:  # 未指定数量,默认1
        config_getSetu.toGetNum = 1
    config_getSetu.tags = [i for i in set(re.split(r"[,， ]", info[1])) if i != ""]
    if info[2]:  # r18关键字
        config_getSetu.level = 1
    else:
        config_getSetu.level = 0
    await Setu(event, bot, config_getSetu)