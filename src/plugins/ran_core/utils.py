import re

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
    temp.pop(-1)
    return "_".join(temp)