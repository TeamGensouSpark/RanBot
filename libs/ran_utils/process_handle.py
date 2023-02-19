import subprocess,sys
class BotRunner:
    def __init__(self,command,std=None,*args,**kwargs) -> None:
        if not std:
            std=sys.stdout
        popen=subprocess.Popen(
                    args=command,
                    shell=True,
                    stdout=std,
                    stderr=std,
                    *args,
                    **kwargs
            )
