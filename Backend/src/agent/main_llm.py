from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from typing import TypedDict,Annotated
from langgraph.graph import StateGraph, START , END
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from config.settings import OLLAMA_MODEL, OLLAMA_NUM_CTX,CHECKPOINT_DB
from memory.profile import path_conn
from tools.lesson import save_lesson

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
llm = ChatOllama(
    model = OLLAMA_MODEL,
    num_ctx = OLLAMA_NUM_CTX,
    streaming = True,
)

def chat_node(state: ChatState) -> ChatState:
    System_msg = SystemMessage(content = path_conn())
    msgs = state["messages"]
    llm_response = llm.invoke([System_msg]+msgs)
    return {"messages": llm_response}

def lesson_node(state: ChatState) -> ChatState:
    llm.bind_tools([save_lesson])
    return {"messages": llm}

conn = sqlite3.connect(CHECKPOINT_DB , check_same_thread=False)
memory_saver = SqliteSaver(conn)

graph = StateGraph(ChatState)
graph.add_node("chatnode" ,chat_node)
graph.add_node("lessonnode", lesson_node)
graph.add_edge(START, "lessonnode")
graph.add_edge("lessonnode", "lessonnode")
graph.add_edge("lessonnode", END)

message_out = graph.compile(checkpointer = memory_saver)

