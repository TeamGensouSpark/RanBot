from ..env import app,bot
from pydantic import BaseModel
from fastapi import Response
from nonebot.adapters.onebot.v11 import Bot
from typing import Optional
class ApiArgs(BaseModel):
    message:Optional[str]="message"
    user_id:Optional[int]=123
    group_id:Optional[int]=123
    is_private:Optional[bool]=False

@app.post("/ranbot/api/command/send")
async def apihandle(args:ApiArgs):
    try:
        if args.is_private:
            await bot().send_private_msg(user_id=args.user_id,message=args.message,auto_escape=False)
        else:
            await bot().send_group_msg(group_id=args.group_id,message=args.message,auto_escape=False)
        return Response(f"post msg success")
    except Exception as e:
        return e