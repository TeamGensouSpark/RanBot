from nonebot.config import Env,Config

jdbpath="src/resources/ran_core/botdb.json"
_botenv=Env()
print("env is",_botenv.environment)
botcfg=Config(_env_file=f'.{_botenv.environment}.env')