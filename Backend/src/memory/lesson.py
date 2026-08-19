from datetime import datetime
from shlex import join
import sys
from config.settings import LESSONS_DIR
from pathlib import Path
import uuid
from shlex import join

def record_event(text):
    path = LESSONS_DIR / "lesson_events.md"
    hash = uuid.uuid4().hex[:6]
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(path, "a" , encoding="utf-8") as f:
        f.write(f"id = {hash} {stamp}: {text}\n")

def lesson_path():
    path = LESSONS_DIR / "lesson_events.md"
    if not path.exists():
        return ""
    return path.read_text(encoding= "utf-8")

def delete_lesson(lesson_id):
    path = LESSONS_DIR/ "lesson_events.md"
    if not path.exists():
        return ""
    kept = []
    removed = False
    for line in path.read_text(encoding = "utf-8").splitlines():
        if line.startswith(f"id = {lesson_id}"):
            removed = True
        else:
            kept.append(line)
    temp = path.with_suffix(".tmp")
    temp.write_text("\n" .join(kept) +"\n" , encoding="utf-8")
    temp.replace(path)
    return removed
