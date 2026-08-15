from langchain_core.tools import  tool
from memory.lesson import record_event


@tool
def save_lesson(lesson :str) -> str:
    """
        This tool is used to tell what is the user stated, how he does the work, how he thinks.
        where and where  he works , etc. This toold basically extracts the user's type based on 
        how he responds or like the output or his characteristics and outputs of how he works and talks with you.

        The tool is called only when you are sure about the user's type and you are sure that he likes
        to do the tasks or accept the outputs in that way. 

        This tool will not be called for silly reasons.

        For example 1: User: stop explaining things I already know.
                       *saves in lesson_events.md*
                       *Archit prefers concise answers, avoid over-explaining*
            example 2: User: I like to do things in a certain way, please follow that.
                       *saves in lesson_events.md*
                       *Archit prefers to do things in a certain way, follow his instructions*
            example 3: *user repeatedly asks for more details and explanations*
                       *saves in lesson_events.md*
                       *Archit prefers detailed explanations, provide more details and explanations*
            example 4: User : I use uv, not pip
                       *saves in lesson_events.md*
                    *Archit prefers to use uv, not pip, use uv for package management*
    """
    record_event(lesson)
    return "Lesson saved successfully."
