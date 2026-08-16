import sys
from pathlib import Path
from langchain_core.messages import HumanMessage
BACKEND_SRC = Path(__file__).parent / "Backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))
from agent.main_llm import message_out
from utils.logs import Logs_path_connector

while True:
    chat_input = input("User: ")
    
    if chat_input.lower() in ["exit jarvis", "quit jarvis", "that's all for today jarvis"]:
        print("Exiting the chat...")
        break

    msg = message_out.invoke(
        {
            "messages": [
                {"role": "user", "content": chat_input}
            ]
            
        },
        config = {"configurable" : {
            "thread_id" : "chat_thread",
        }},
        )

    tool_call = []
    for i in reversed(msg["messages"]):
        if isinstance(i , HumanMessage):
            break
        value = getattr(i , "tool_calls" , None)
        if value: 
            tool_call.append(value)


    chat_output = msg["messages"][-1].content  
    Logs_path_connector( chat_input ,chat_output , tool_call)
    print(chat_output)