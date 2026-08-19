from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode , tools_condition
import sqlite3
from typing import TypedDict,Annotated
from langgraph.graph import StateGraph, START , END
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from config.settings import OLLAMA_MODEL, OLLAMA_NUM_CTX,CHECKPOINT_DB
from memory.profile import path_conn
from memory.lesson import lesson_path , delete_lesson
from tools.lesson import save_lesson

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOllama(
    model = OLLAMA_MODEL,
    num_ctx = OLLAMA_NUM_CTX,
    streaming = True,
)

def chat_node(state: ChatState) -> ChatState:
    System_msg = SystemMessage(content = f"""'About the user'
                                         {path_conn()}

                                         Learned preferences — follow these strictly
                                         {lesson_path()}
                                """)
    msgs = state["messages"]
    lesson_tool = llm.bind_tools([save_lesson] , [delete_lesson])
    llm_response = lesson_tool.invoke([System_msg]+msgs)
    return {"messages": llm_response}

conn = sqlite3.connect(CHECKPOINT_DB , check_same_thread=False)
memory_saver = SqliteSaver(conn)

graph = StateGraph(ChatState)
graph.add_node("chatnode" ,chat_node)
graph.add_node("tools", ToolNode([save_lesson , delete_lesson]))

graph.add_edge(START, "chatnode")
graph.add_conditional_edges("chatnode" , tools_condition)
graph.add_edge("tools" , "chatnode")

message_out = graph.compile(checkpointer = memory_saver)
