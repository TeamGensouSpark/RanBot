if __name__ == "__main__":
    from libs import ran_utils
    from multiprocessing import Process
    import os
    import importlib
    from colorama import Fore
    for path,name in zip(["./libs/ext/"+_ for _ in os.listdir("libs/ext")],[_ for _ in os.listdir("libs/ext")]):
        importlib.import_module(f".ext.{name}",package="libs")
        print(f"[ Boot ]{Fore.LIGHTGREEN_EX}import ext: {Fore.LIGHTRED_EX+path} {Fore.LIGHTGREEN_EX}as {Fore.LIGHTRED_EX+name} {Fore.LIGHTGREEN_EX}success")

    botProcess=Process(target=ran_utils.process_handle.BotRunner,args=("nb run",))
    botProcess.start()
    ran_utils.commands.BOT_PROCESS=botProcess
    while True:
        try:
            print(ran_utils.commands.BOT_PROCESS,"boot process launched successfully")
            break
        except:
            pass

    while True:
        ran_utils.commands.Command_parser(input("boot@command: "))