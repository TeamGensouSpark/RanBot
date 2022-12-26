from ...ran_utils.commands import CommandClass,Command_parser
from Remilia.lite.LiteMixin import InjectClass

@InjectClass(Command_parser)
class bot(CommandClass):
    def install(self,plugin_name:str):
        print("inject")
    def __desc__(self):
        super().__desc__()
        return {
            "install":"to install a bot plugin"
        }
    def __selfdesc__() -> str:
        return "A ext plugin to contorl bot plugin😀"