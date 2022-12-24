from libs import ran_utils
from multiprocessing import Process

if __name__ == "__main__":
    botProcess=Process(target=ran_utils.process_handle.Process,args=("nb run",))
    botProcess.start()
    ran_utils.commands.BOT_PROCESS=botProcess
    while True:
        try:
            print(ran_utils.commands.BOT_PROCESS,"boot process launched successfully")
            
            break
        except:
            pass

    while True:
        ran_utils.commands.Command_parser(input(""))