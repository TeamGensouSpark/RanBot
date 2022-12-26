from pixivpy_async.sync import AppPixivAPI
from Remilia.utils.cli import prompts
from Remilia.utils.cli.prompts import Choice
from Remilia.lite.LiteResource import File
from nonebot.config import Env,Config
import json

appi=AppPixivAPI(bypass=True)
envfile=".env.%s"%Env().environment
config=Config(envfile=envfile)
def setuptoken():
    auth=appi.login_web()
    refresh_token=auth["refresh_token"]
    File(envfile).write("a","\nPIXIVTOKEN=\"%s\""%refresh_token)
    print("配置成功")
def setuplibs():
    pass


pmt=prompts.ListPrompt("选择配置对象",[
    Choice("Pixiv Token",data=setuptoken),
    Choice("Setup Bot",data=setuplibs)
]).prompt().data()