from langchain_core.tools import  tool
from memory.lesson import record_event , update_lesson , delete_lesson

@tool
def save_lesson(lesson :str) -> str:
    """Record a durable fact about how this user works, so future responses match it.

        A lesson is a STANDING preference, constraint, or environment fact. It is not
        a one-off instruction about the current task.

        DURABILITY TEST -- the single question that decides this call:
          "Would this change how I respond to a DIFFERENT task, next week?"
          Yes -> save. No -> task context, not a lesson. Do not save.

        TRIGGER TEST -- call this only when ALL are true:
          (a) The durability test passes, AND
          (b) EITHER the user stated it explicitly (once is enough), OR you have
              observed the same unstated pattern in at least THREE separate turns, AND
          (c) No stored lesson already covers it.

        Args:
            lesson: The lesson text, obeying ALL of these:
                - Third person, naming the user: "Archit uses uv, not pip."
                - Standalone. Understandable with zero conversation context.
                - Actionable. Name the behavior to change, not just an observation.
                  "Archit prefers concise answers" is too vague.
                  "Archit wants answers that skip explanation of concepts he already
                  knows" is actionable.
                - Scoped if conditional: "...for Rust code", "...in code reviews".
                - Exactly ONE preference. Two preferences -> two calls.

        DO NOT call this tool when:
          - The instruction applies only to the current output: "make this one
            shorter", "just the docstring this time", "skip the preamble here".
          - The lesson would be vacuous. Anything of the form "the user likes things
            done a certain way" carries no information and is worse than saving
            nothing.
          - The user is describing a one-time situation, a deadline, or a mood.
          - You are inferring from a SINGLE ambiguous signal.
          - A stored lesson already says this. A near-duplicate is a failure.
          - A stored lesson CONTRADICTS this -> call update_lesson_tool on that
            lesson instead of stacking a second, conflicting one.

        EXAMPLES

          User: "I use uv, not pip."
          -> save_lesson("Archit uses uv for Python package management, not pip.")

          User: "stop explaining things I already know"
          -> save_lesson("Archit wants answers that omit background explanation of
             concepts he has already demonstrated familiarity with.")

          User: "always give me the tradeoffs, don't just tell me the happy path"
          -> save_lesson("Archit wants explicit tradeoffs and failure modes stated
             alongside any recommendation.")

        COUNTER-EXAMPLES (do NOT call this tool)

          User: "only give me the docstring, nothing else"
          -> Scoped to this one response. Task instruction, not a standing preference.

          User: "I like to do things a certain way, please follow that."
          -> Vacuous. No behavior is named. Ask what specifically, or save nothing.

          User: "can you go deeper on that?" (first occurrence)
          -> Single signal. Wait for a third before inferring a depth preference.

          User: "I'm swamped this week, keep it brief."
          -> Temporary condition, not a durable preference.
        """

    record_event(lesson)
    return "Lesson saved successfully."

@tool
def delete_lesson_tool(lesson_id: str) -> str:
    """Permanently remove a stored lesson that is no longer true.

       This is IRREVERSIBLE. Prefer update_lesson_tool whenever a corrected version
       of the fact exists.

       TRIGGER TEST -- call this only when ALL are true:
         (a) the user explicitly retracts or invalidates a stored lesson, AND
         (b) the user supplies NO replacement fact, AND
         (c) exactly one known lesson matches the retraction.

       Before calling, state in your reasoning which span of the user's message
       constitutes the retraction. If you cannot point to a literal retraction, the
       user did not ask for a deletion and you must not call this tool.

       Args:
           lesson_id: The exact `id` string of a lesson shown to you EARLIER IN THIS
               CONVERSATION. Copy it character for character. Never invent or guess
               an ID.

       DO NOT call this tool when:
         - The user provides a corrected version -> use update_lesson_tool.
         - No lesson with this ID was shown to you earlier in this conversation.
         - The retraction is hedged: "I think that's wrong", "that might be
           outdated". Ask the user to confirm before deleting.
         - Several known lessons could match. Ask which one.
         - The user is annoyed at a response and venting. Frustration is not a
           retraction.

       EXAMPLES

         Known: [id = a71d6f : "Archit uses pip for packages."]
         User: "Drop the pip thing entirely, it's not true anymore."
         -> delete_lesson_tool(lesson_id="a71d6f")

       COUNTER-EXAMPLES (do NOT call this tool)

         Known: [id = a71d6f : "Archit uses pip for packages."]
         User: "I use uv now."
         -> A replacement exists. Call update_lesson_tool.

         Known: [{id = 503e05 : "Archit wants concise answers."},
                 {id = e0437f : "Archit wants tradeoffs stated."}]
         User: "that preference doesn't apply anymore"
         -> Ambiguous target. Ask which one.

         Known: [{id = 503e05 : "Archit wants concise answers."}]
         User: "this answer is useless"
         -> Criticism of one output, not a retraction of the lesson.
       """
    delete_lesson(lesson_id = lesson_id)
    return "Lesson deleted successfully."


@tool
def update_lesson_tool(lesson_id: str, text: str) -> str:
    """Replace a stored lesson's text with a corrected version.

        TRIGGER TEST -- call this only when BOTH are true of the user's message:
          (a) it indicates a stored lesson is wrong, stale, or incomplete, AND
          (b) it supplies the corrected information that should replace it.

        If (b) is missing, this is a retraction, not a correction -> use
        delete_lesson_tool instead.

        Args:
            lesson_id: The exact `id` string of a lesson shown to you EARLIER IN THIS
                CONVERSATION. Copy it character for character. Never invent, guess,
                abbreviate, or reformat an ID. If no lesson with that ID appears in
                this conversation, you do not have a valid ID and must not call this
                tool.
            text: The COMPLETE replacement text, written as a standalone statement in
                third person. Not a diff, not a fragment, not a reference such as
                "same as before but uv". A reader with no other context must be able
                to understand it.

        DO NOT call this tool when:
          - No lesson with this ID was shown to you earlier in this conversation.
          - Two or more known lessons could plausibly be the target. Ask which one.
          - The user states a fact that does not contradict anything stored. That is
            a new lesson -> call save_lesson.
          - The user is asking a question rather than asserting a correction.

        EXAMPLES

          Known: [id = a71d6f : "Archit uses pip for packages."]
          User: "I moved everything to uv."
          -> update_lesson_tool(lesson_id = a71d6f,
                                text="Archit uses uv for Python package management.")

          Known: [id = 503e05 : "Archit wants detailed explanations."]
          User: "Actually cut the explanations, just give me the code."
          -> update_lesson_tool(lesson_id = 503e05,
                                text="Archit wants code-first answers with minimal
                                surrounding explanation.")

        COUNTER-EXAMPLES (do NOT call this tool)

          Known: [id = a71d6f : "Archit uses pip for packages."]
          User: "I don't use pip anymore."
          -> No replacement given. Call delete_lesson_tool.

          Nothing shown yet.
          User: "that preference of mine is outdated"
          -> No grounded ID. Ask which lesson they mean.

          Known: [id = a71d6f : "Archit uses uv."]
          User: "wait, do I have a package manager preference saved?"
          -> A question, not a correction. Answer from the known text.
        """

    update_declare = update_lesson(lesson_id = lesson_id, text = text)
    if update_declare == "updated":
        return update_declare
    else:
        update_declare = "created."
    return update_declare
