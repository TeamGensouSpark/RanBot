from Remilia.fancy import ifElse

if True:
    from nonebot.adapters.onebot.v11 import (
        MessageEvent as OBV11_MessageEvent,
        MessageSegment as OBV11_MessageSegment,
        Message as OBV11_Message,
        GroupMessageEvent as OBV11_GroupMessageEvent,
    )

MessageEvent = OBV11_MessageEvent
Message = OBV11_Message
MessageSegment = OBV11_MessageSegment
GroupMessageEvent = OBV11_GroupMessageEvent


def isGroupMessage(msge: MessageEvent):
    return isinstance(msge, GroupMessageEvent)

def genSessionUUID(msge: MessageEvent) -> str:
    if isinstance(msge, OBV11_MessageEvent):
        return (
            "qqgroup:%s" % msge.group_id
            if isGroupMessage(msge)
            else "qquser:%s" % msge.user_id
        )
    return "undefined:%s" % msge.get_session_id()
