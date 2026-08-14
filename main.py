import sys
from pathlib import Path

BACKEND_SRC = Path(__file__).parent / "Backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from agent.main_llm import message_out

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
    print(msg["messages"][-1].content)