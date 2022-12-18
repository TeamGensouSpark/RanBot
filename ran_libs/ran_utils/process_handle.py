import subprocess,sys
class Process:
    def __init__(self,command,*args,**kwargs) -> None:
        popen=subprocess.Popen(
                    args=command,
                    shell=True,
                    stdout=sys.stdout,
                    stderr=sys.stdout,
                    *args,
                    **kwargs
            )
