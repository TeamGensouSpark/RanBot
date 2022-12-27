from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent,Bot,GROUP_ADMIN,GROUP_OWNER,GroupMessageEvent
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from .env import jdb

if not jdb.hasTable("groupmanage"):
    jdb.createTable("groupmanage")
    jdb.getTable("groupmanage").setkey("welcome",{}).setkey("keywords",{}).sync()


async def welcome(event:GroupIncreaseNoticeEvent,bot:Bot):
    if jdb.getTable("groupmanage").haskey(event.group_id):
        await bot.send_group_msg(jdb.getTable("groupmanage").getkey(event.group_id))

setwelcome=on_command(cmd="setwelcome",rule=to_me(),aliases={"设置入群欢迎"},priority=5)
@setwelcome.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if await GROUP_ADMIN(bot, event):
        await setwelcome.send("todo")
    elif await GROUP_OWNER(bot, event):
        await setwelcome.send("todo")
    else:
        pass