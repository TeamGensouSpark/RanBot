import re
from typing import List, Union
from nonebot.adapters.onebot.v11 import MessageEvent,Message,PrivateMessageEvent
from nonebot import get_driver

global_config = get_driver().config


def get_config(configname:str,default:any):
    try:
        return getattr(global_config,configname)
    except:
        return default
    
nickname=get_config("nickname","bot")
if isinstance(nickname,set):
    try:
        nickname=list(nickname)[0]
    except:
        nickname=nickname

def get_session_oid(event:MessageEvent):
    return event.user_id if isinstance(event,PrivateMessageEvent) else event.group_id
    
    
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