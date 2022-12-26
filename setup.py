from pixivpy_async.sync import AppPixivAPI
from Remilia.utils.cli import prompts
from Remilia.utils.cli.prompts import Choice
from Remilia.lite.LiteResource import File
import json

appi=AppPixivAPI(bypass=True)

def setuptoken():
    auth=appi.login_web()
    refresh_token=auth["refresh_token"]
    File("src/plugins/nonebot-plugin-setu/.PixivToken.json").write("w",json.dumps({"refresh_token":refresh_token},indent=4))
    print("配置成功")
def setuplibs():
    pass


pmt=prompts.ListPrompt("选择配置对象",[
    Choice("Pixiv Token",data=setuptoken),
    Choice("Setup Bot",data=setuplibs)
]).prompt().data()