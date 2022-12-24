import os,json
from signal import SIGINT,SIGILL
import multiprocessing
from Remilia.jsondb.db import JsonDB,File
from .env import jdbpath,botcfg
import requests
from Remilia.lite.LiteFunctions import typedet
BOT_PROCESS:multiprocessing.Process
class CommandClass:
    def __init__(self,command,*args,**kwargs) -> None:
        self.jdb=JsonDB(File(jdbpath),None)
        if command in dir(self):
            getattr(self,command)(*args,**kwargs)
class Command_parser:
    def __init__(self,command:str) -> None:
        self.parse_command(command)
        
    def parse_command(self,command:str):
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
    def help(self):
        print(
            '''
             
↓RAN'S Command Help↓
            
1.help : use help to get some useless help
2.stop : use it to stop bot(may not work in windows)
3.restart : use it to stop bot and restart
4.start : use it to start nonebot
            
            '''
        )
    def stop(self):
        print("start stop thread...")
        os.kill(BOT_PROCESS.pid,SIGINT)
        print("start successfully")
    def start(self):
        pass
    
    def post(self,url,data):
        data=typedet(data,False)
        rep=requests.post(url,data=json.dumps(data))
        print(rep.text)
    class jdb(CommandClass):
        def create(self,tablename:str):
            self.jdb.createTable(tablename)
            print(f"table '{tablename}' success")
        
        def listtable(self):
            for _ in self.jdb.listTable():
                print(_)
        
        def read(self,tablename:str,key:str):
            print(self.jdb.getTable(tablename).getkey(key))
    
    class qq(CommandClass):
        def sendgroup(self,groupid,message):
            api="http://"+str(botcfg.host)+":"+str(botcfg.port)+"/ranbot/api/command/send"
            data={
                'message':message,
                'group_id':groupid
            }
            rep=requests.post(api,data=json.dumps(data))
            print(rep)
        def senduser(self,userid,message):
            api="http://"+str(botcfg.host)+":"+str(botcfg.port)+"/ranbot/api/command/send"
            data={
                'message':message,
                'user_id':userid,
                'is_private':True
            }
            rep=requests.post(api,data=json.dumps(data))
            print(rep.text)