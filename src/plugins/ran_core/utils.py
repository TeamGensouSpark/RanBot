import re
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot import get_driver
global_config = get_driver().config

def convImg(raw:str):
    from nonebot.adapters.onebot.v11 import MessageSegment,Message
    if re.search(r"\[CQ:image,file.*]",raw):
        repindex=re.findall(rf"\[CQ:image,file=.*?url=(.*?)]",raw)
        rep=re.split(rf"\[CQ:image,file=.*?url=(.*?)]",raw)
        for reprep,index in zip(rep,range(len(rep))):
            if reprep in repindex:
                rep[index]=MessageSegment.image(file=reprep)
    else:
        rep=raw
    return Message(rep)

def exgroupid(session_id:str):
    temp=session_id.split("_")
    if len(temp) == 1:
        return temp[0]
    else:
        temp.pop(-1)
        return "_".join(temp)
    
def getex_session_id(event:MessageEvent):
    return exgroupid(event.get_session_id())

def get_config(configname:str,default:any):
    try:
        return getattr(global_config,configname)
    except:
        return default