from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot import on_message,on_command
from nonebot.rule import to_me
from nonebot.params import ArgPlainText
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from .env import jdb
from .utils import exgroupid

async def priorAll(event:MessageEvent):
    print(exgroupid(event.get_session_id()) not in jdb.getTable("auth")["auth_session"])
    return exgroupid(event.get_session_id()) not in jdb.getTable("auth")["auth_session"]


authblock=on_message(rule=priorAll,priority=2,block=True)
    

@authblock.handle()
async def handle(matcher: Matcher,event:MessageEvent):
    pass

auth=on_command(cmd="auth",aliases={"授权"},rule=to_me(),priority=1,permission=SUPERUSER)
@auth.got("confirm",prompt="确定授权吗(Y/N)")
async def gotarg(matcher: Matcher,event:MessageEvent,confirm=ArgPlainText("confirm")):
    if confirm == "Y":
        table=jdb.getTable("auth")
        table["auth_session"].append(exgroupid(event.get_session_id()))
        jdb.updateTable(table)
        await auth.finish("授权成功")
    else:
        await auth.finish("已取消") 