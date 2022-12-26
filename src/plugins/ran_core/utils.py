import re
from typing import List, Union
from nonebot.adapters.onebot.v11 import MessageEvent,Message
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
    
nickname=get_config("nickname","bot")
if isinstance(nickname,set):
    nickname=list(nickname)[0]
def custom_forward_msg(
        msg_list: List[Union[str, Message]], uin: Union[int, str], name: str = f"这里是{nickname}"
) -> List[dict]:
    """
    说明:
        生成自定义合并消息
    参数:
        :param msg_list: 消息列表
        :param uin: 发送者 QQ
        :param name: 自定义名称
    """
    uin = int(uin)
    mes_list = []
    for _message in msg_list:
        data = {
            "type": "node",
            "data": {
                "name": name,
                "uin": f"{uin}",
                "content": _message,
            },
        }
        mes_list.append(data)
    return mes_list