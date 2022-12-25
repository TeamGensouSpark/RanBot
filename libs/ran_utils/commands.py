import os,json
from signal import SIGINT,SIGILL
import multiprocessing
from Remilia.jsondb.db import JsonDB,File
from .env import jdbpath,botcfg
import requests
from Remilia.lite.LiteFunctions import typedet
BOT_PROCESS:multiprocessing.Process
class CommandClass:
    def __init__(self,command=None,*args,**kwargs) -> None:
        if command in dir(self):  
            getattr(self,command)(*args,**kwargs)
        else:
            print(f"unknown command,use '{self.__class__.__name__} help' for help")
    def __cmddescf__(self,command):
        desc=self.__desc__()
        if command in desc:
            return desc[command]
        try:
            if issubclass(getattr(self,command),CommandClass):
                return getattr(getattr(self,command),"__selfdesc__")()
        except:
            pass
        return "None"

    def __selfdesc__() -> str:
        return "None"
    
    def __desc__(self):
        return {}
    
    def help(self):
        print("the command class has these commands👇")
        print("\n".join([' · '+_+f': {self.__cmddescf__(_)}' for _ in dir(self) if not _.startswith("__") and not _.startswith("_")]))
    
class Command_parser(CommandClass):
    def __init__(self,command:str) -> None:
        self.__parse_command(command)
    def __parse_command(self,command:str):
        tasklist=command.split(" ")
        command=tasklist[0]
        if len(tasklist) > 1:
            args=tasklist[1:]
        else:
            args=[]
        if command not in dir(self):
            print("unknown command,use 'help' to get help")
        else:
            try:
                getattr(self,command)(*args)
            except Exception as e:
                print(e)
    def __desc__(self):
        return {
            "help" : "use help to get some useless help",
            "stop" : "use it to stop bot(may not work in windows)",
            "restart" : "use it to stop bot and restart(may not work in windows)",
            "start" : "use it to start nonebot(may not work in windows)"
        }
    def stop(self):
        print("start stop thread...")
        os.kill(BOT_PROCESS.pid,SIGINT)
        print("start successfully")
    def start(self):
        pass
    def post(self,url,post_type,data):
        data=typedet(data,False)
        if post_type=="data":
            rep=requests.post(url,data=json.dumps(data))
        else:
            rep=requests.post(url,data=json.dumps(data))
        print(rep.text)
        
    class jdb(CommandClass):
        def __init__(self, command=None, *args, **kwargs) -> None:
            self._jdb=JsonDB(File(jdbpath),None)
            super().__init__(command, *args, **kwargs)
        def create(self,tablename:str):
            self._jdb.createTable(tablename)
            print(f"create table '{tablename}' success")
        def listtable(self):
            print("\n".join([' · '+_ for _ in self._jdb.listTable()]))
        def read(self,tablename:str,key:str):
            print(self._jdb.getTable(tablename).getkey(key))
        def __selfdesc__() -> str:
            return "a command to operate jsondb(the bot db)"
    class qq(CommandClass):
        def sendgroup(self,groupid,message):
            api="http://"+str(botcfg.host)+":"+str(botcfg.port)+"/ranbot/api/command/send"
            data={
                'message':message,
                'group_id':groupid
            }
            rep=requests.post(api,data=json.dumps(data))
            print(rep.text+f"<Code {rep.status_code}>")
        def senduser(self,userid,message):
            api="http://"+str(botcfg.host)+":"+str(botcfg.port)+"/ranbot/api/command/send"
            data={
                'message':message,
                'user_id':userid,
                'is_private':True
            }
            rep=requests.post(api,data=json.dumps(data))
            print(rep.text+f"<Code {rep.status_code}>")
        
        def __desc__(self):
            return {
                "senduser":"a command send msg to user in private",
                "sendgroup":"a command send msg to a group"
            }
        def __selfdesc__() -> str:
            return "a command to operate qq by api"