from nonebot import on_command
from nonebot.rule import to_me
from RanLib.event import MessageSegment, MessageEvent
from RanLib.markdoven import MarkDovenClient
from RanLib.database import CateRanCore
from Remilia.fancy import StringBuilder as SBr
from datetime import datetime, timedelta

daysign = on_command("daysign", aliases={"签到"}, priority=5, rule=to_me())

DAYSIGN = CateRanCore.getTable("DAYSIGN")


def is_same_day(timestamp1, timestamp2):
    d1 = datetime.fromtimestamp(timestamp1)
    d2 = datetime.fromtimestamp(timestamp2)
    return d1.date() == d2.date() and abs(d1 - d2) <= timedelta(hours=24)


@daysign.handle()
async def daysignhandle(msge: MessageEvent):
    user_id = msge.get_user_id()
    info: dict
    if DAYSIGN.hasKey(user_id):
        info = DAYSIGN.readValue(user_id)
        if is_same_day(info["last"], datetime.now().timestamp()):
            await daysign.finish("你今天已经签过了😅")
        else:
            info.update({"keep": info["keep"] + 1})
    else:
        info = {"last": datetime.now().timestamp(), "keep": 1}
    DAYSIGN.writeKV(user_id, info)

    await daysign.finish(
        MessageSegment.image(
            await MarkDovenClient.instance.renderText(
                text=str(
                    SBr()
                    .concat("# 签到 🥰")
                    .newline.newline.concat("---")
                    .newline.newline.concat(
                        "%s，您总计签到%s天🎉" % (msge.get_user_id(), info["keep"])
                    )
                ),
                isdark=True,
            )
        )
    )
