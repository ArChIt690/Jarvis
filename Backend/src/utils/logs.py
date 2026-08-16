import sys
from pathlib import Path
from config.settings import LOGS_DIR
from datetime import datetime


def Logs_path_connector(chat_input , chat_ouput , tool_call):

    path = LOGS_DIR / "LOGS.md"
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open (path , "a" , encoding="utf-8" ) as f:
        f.write(f"{stamp} : {chat_input}\n {chat_ouput}\n {tool_call} \n\n" )
