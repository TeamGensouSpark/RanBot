from RanLib.database import CateRanCore
from RanLib.event import MessageEvent, genSessionUUID
from Remilia.fancy import when
from nonebot import on_message, on_command
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

PERMISSION = CateRanCore.getTable("PERMISSION")
when(not PERMISSION.hasKey("whitelist"), lambda: PERMISSION.writeKV("whitelist", []))
when(not PERMISSION.hasKey("blacklist"), lambda: PERMISSION.writeKV("blacklist", []))


async def blockRuler(msge: MessageEvent):
    return genSessionUUID(msge) not in PERMISSION.readValue(
        "whitelist"
    ) or genSessionUUID(msge) in PERMISSION.readValue("blacklist")


_Invoke = on_message(priority=2, rule=blockRuler, block=True)


@_Invoke.handle()
async def _():
    pass


auth = on_command(
    cmd="auth", aliases={"授权"}, priority=1, permission=SUPERUSER, rule=to_me()
)
unauth = on_command(
    cmd="unauth", aliases={"取消授权"}, priority=1, permission=SUPERUSER, rule=to_me()
)


@auth.handle()
async def auth_handle(msge: MessageEvent):
    wl = PERMISSION.readValue("whitelist")
    sid = genSessionUUID(msge)
    if sid not in wl:
        wl.append(sid)
        PERMISSION.writeKV("whitelist", wl)
        await auth.finish("授权成功😋")
    else:
        await auth.finish("该会话已授权😅")



@unauth.handle()
async def unauth_handle(msge: MessageEvent):
    wl = PERMISSION.readValue("whitelist")
    sid = genSessionUUID(msge)
    if sid in wl:
        wl.remove(sid)
        PERMISSION.writeKV("whitelist", wl)
        await auth.finish("已取消授权😋")
    else:
        await auth.finish("该会话未授权😅")


deny = on_command(
    "deny", aliases={"拉黑"}, priority=1, permission=SUPERUSER, rule=to_me()
)
undeny = on_command(
    "undeny", aliases={"取消拉黑"}, priority=1, permission=SUPERUSER, rule=to_me()
)


@deny.handle()
async def deny_handle(msge: MessageEvent):
    bl = PERMISSION.readValue("blacklist")
    sid = genSessionUUID(msge)
    if sid not in bl:
        bl.append(sid)
        PERMISSION.writeKV("blacklist", bl)
        await auth.finish("已拉黑😋")
    else:
        await auth.finish("该会话已拉黑😅")


@undeny.handle()
async def undeny_handle(msge: MessageEvent):
    bl = PERMISSION.readValue("blacklist")
    sid = genSessionUUID(msge)
    if sid in bl:
        bl.remove(sid)
        PERMISSION.writeKV("blacklist", bl)
        await auth.finish("已取消拉黑😋")
    else:
        await auth.finish("该会话未拉黑😅")