import os,sys
if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    mode="default"
try:
    from Remilia.utils.cli import prompts
    from Remilia.utils.cli.prompts import Choice
    from Remilia.lite.LiteResource import File
except Exception as e:
    print(e)
    print("必要组件未安装")
    if mode=="cn":
        os.system("pip install Remilia -i https://pypi.tuna.tsinghua.edu.cn/simple")
    else:
        if input("是否使用国内镜像源(y/x)") == "y":
            os.system("pip install Remilia -i https://pypi.tuna.tsinghua.edu.cn/simple")
        else:
            os.system("pip install Remilia")
    input("安装完成，请重启该程序")
    exit()
import os
if not os.path.exists("src/resources"):
    os.makedirs("src/resources")
    File("src/resources/additional_plugins.txt").write("w","")
def setuptoken():
    from pixivpy_async.sync import AppPixivAPI
    from nonebot.config import Env,Config
    appi=AppPixivAPI(bypass=True)
    auth=appi.login_web()
    refresh_token=auth["refresh_token"]
    File(".env.%s"%Env().environment).write("a","\nPIXIVTOKEN=\"%s\""%refresh_token)
    print("配置成功")
def setupnbgc():
    if  mode=="cn":
        os.system("pip install nonebot-plugin-gocqhttp -i https://pypi.tuna.tsinghua.edu.cn/simple")
    else:
        if prompts.ConfirmPrompt("是否使用国内镜像").prompt():
            os.system("pip install nonebot-plugin-gocqhttp -i https://pypi.tuna.tsinghua.edu.cn/simple")
        else:
            os.system("pip install nonebot-plugin-gocqhttp")
    if "nonebot-plugin-gocqhttp" not in File("src/resources/additional_plugins.txt").text:
        File("src/resources/additional_plugins.txt").write("a","nonebot_plugin_gocqhttp\n")
    
def lazysetup():
    if mode == "cn":
        os.system("pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple")
    else:
        os.system("pip install -r requirements.txt")
    setupnbgc()
    File(".env").write("w","# .env\nENVIRONMENT=prod")
    print("配置完成,接下来按照以下步骤进行")
    print("1.打开 .env.prod 配置 SUPERUSER（QQ号 例如 SUPERUSERS=[\"123114124\"]）")
    print("2.终端运行 python ./boot.py")
    print("3.等待加载插件完成打开 http://127.0.0.1:8080/go-cqhttp 添加账户")
    input()
    
pmt=prompts.ListPrompt("选择配置对象",[
    Choice("Pixiv Token",data=setuptoken),
    Choice("Setup nonebot-plugin-gocqhttp",data=setupnbgc),
    Choice("Lazy Setup(include nonebot-plugin-gocqhttp)",data=lazysetup)
]).prompt().data()