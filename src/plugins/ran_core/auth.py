from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot import on_message,on_command
from nonebot.rule import to_me
from nonebot.params import ArgPlainText
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER

from ..ran_utils.env import db
from ..ran_utils.utils import get_session_oid

try:
    db.get_file("auth")
except:
    db.createfile("auth")
    db.writekv("auth","auth_session",[])
    db.writekv("auth","userblock",[])
    
async def checkauth(event:MessageEvent):
    return get_session_oid(event) not in db.readkv("auth","auth_session")

async def checkblock(event:MessageEvent):
    return event.get_user_id() in db.readkv("auth","userblock")

authblock=on_message(rule=checkauth,priority=2,block=True)
userblock=on_message(rule=checkblock,priority=2,block=True)


@userblock.handle()
async def handle():pass
@authblock.handle()
async def handle():pass

auth=on_command(cmd="auth",aliases={"授权"},rule=to_me(),priority=1,permission=SUPERUSER)
@auth.got("confirm",prompt="确定授权吗(Y/N)")
async def gotarg(matcher: Matcher,event:MessageEvent,confirm=ArgPlainText("confirm")):
    if confirm == "Y":
        if get_session_oid(event) in db.readkv("auth","auth_session"):
            await auth.finish("该会话已授权")
        else:
            aslist=db.readkv("auth","auth_session")
            aslist.append(get_session_oid(event))
            db.writekv("auth","auth_session",aslist)
            await auth.finish("授权成功")
    else:
        await auth.finish("已取消")
        
blockuser=on_command(cmd="blockuser",aliases={"屏蔽用户"},rule=to_me(),priority=1,permission=SUPERUSER)
@blockuser.got("user",prompt="输入目标用户")
async def handle(matcher: Matcher,event:MessageEvent,user=ArgPlainText("user")):
    bklist=db.readkv("auth","userblock")
    bklist.append(user)
    db.writekv("auth","userblock",bklist)
    await auth.finish(f"已屏蔽用户{user}")

unauth=on_command(cmd="unauth",aliases={"取消授权"},rule=to_me(),priority=1,permission=SUPERUSER)
@unauth.handle()
async def gotarg(matcher: Matcher,event:MessageEvent):
    table=db.readdict("auth")
    try:
        table["auth_session"].remove(get_session_oid(event))
        db.writedict("auth",table)
        await auth.finish("已成功取消")
    except:
        await auth.finish("未在授权列表内")