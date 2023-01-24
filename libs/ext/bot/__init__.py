from ...ran_utils.commands import CommandClass,Command_parser
from Remilia.lite.LiteResource import File
from Remilia.lite.LiteMixin import InjectClass
from os import system


@InjectClass(Command_parser)
class bot(CommandClass):
    def install(self,plugin_name:str):
        system(f"pip install {plugin_name}")
        f=File("./src/resources/additional_plugins.txt")
        fl=f.text.splitlines()
        if plugin_name not in fl:
            fl.append(plugin_name)
            f.write("w","\n".join(fl))
    def upgrade(self,plugin_name:str):
        system(f"pip install --upgrade {plugin_name}")
    def uninstall(self,plugin_name:str):
        system(f"pip uninstall {plugin_name}")
        f=File("./src/resources/additional_plugins.txt")
        fl=f.text.splitlines()
        if plugin_name in fl:
            fl.remove(plugin_name)
            f.write("w","\n".join(fl))
    def remove(self,plugin_name:str):
        f=File("./src/resources/additional_plugins.txt")
        fl=f.text.splitlines()
        if plugin_name in fl:
            fl.remove(plugin_name)
            f.write("w","\n".join(fl))
    def show(self):
        f=File("./src/resources/additional_plugins.txt")
        print(" · "+"\n · ".join(f.text.splitlines()))
    def __desc__(self):
        super().__desc__()
        return {
            "install":"to install a bot plugin",
            "uninstall":"to uninstall a bot plugin(also pip uninstall)",
            "upgrade":"just use pip to upgrade lib",
            "show":"show all plugin (will be) loaded now",
            "remove":"remove a plugin from bot but not python lib"
        }
    def __selfdesc__() -> str:
        return "A ext plugin to contorl bot plugin😀"