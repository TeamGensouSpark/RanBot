from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent,Bot,GROUP_ADMIN,GROUP_OWNER,GroupMessageEvent,Message
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg,ArgPlainText,Arg
from nonebot.permission import SUPERUSER
from ..ran_utils.env import jdb

if not jdb.hasTable("groupwelcome"):
    jdb.createTable("groupwelcome")


async def welcome(event:GroupIncreaseNoticeEvent,bot:Bot):
    if jdb.getTable("groupwelcome").haskey(event.group_id):
        await bot.send_group_msg(jdb.getTable("groupwelcome").getkey(event.group_id),auto_escape=False)

setwelcome=on_command(cmd="setwelcome",rule=to_me(),aliases={"设置入群欢迎"},priority=5)
@setwelcome.handle()
async def _(matcher:Matcher,args:Message=CommandArg()):
    text=args.extract_plain_text()
    if text:
        matcher.set_arg("stwc",text)

@setwelcome.got("stwc",prompt="输入欢迎词")
async def _(bot: Bot, event: GroupMessageEvent,text=Arg("stwc")):
    text=str(text)
    if await GROUP_ADMIN(bot, event):
        jdb.getTable("groupwelcome").setkey(event.group_id,text).sync()
        await setwelcome.finish("添加成功")
    elif await GROUP_OWNER(bot, event):
        jdb.getTable("groupwelcome").setkey(event.group_id,text).sync()
        await setwelcome.finish("添加成功")
    elif await SUPERUSER(bot, event):
        jdb.getTable("groupwelcome").setkey(event.group_id,text).sync()
        await setwelcome.finish("添加成功")

delwelcome=on_command(cmd="delwelcome",rule=to_me(),aliases={"删除入群欢迎"},priority=5)
@delwelcome.handle()
async def _(bot: Bot, event: GroupMessageEvent,text=ArgPlainText("stwc")):
    if await GROUP_ADMIN(bot, event):
        jdb.getTable("groupwelcome").delkey(event.group_id).sync()
        await setwelcome.finish("删除成功")
    elif await GROUP_OWNER(bot, event):
        jdb.getTable("groupwelcome").delkey(event.group_id).sync()
        await setwelcome.finish("删除成功")
    elif await SUPERUSER(bot, event):
        if jdb.getTable("groupwelcome").haskey(event.group_id):
            jdb.getTable("groupwelcome").delkey(event.group_id).sync()
        await setwelcome.finish("删除成功")