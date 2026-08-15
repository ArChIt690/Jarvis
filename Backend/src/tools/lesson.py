from langchain_core.tools import  tool
from memory.lesson import record_event


@tool
def decision_to_call_tool(decision :str) -> str:
    