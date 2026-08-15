from datetime import datetime
import sys
from config.settings import LESSONS_DIR
from pathlib import Path

def record_event(text):
    path = LESSONS_DIR / "lesson_events.md"
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(path, "a" , encoding="utf-8") as f:
        f.write(f"{stamp}: {text}\n")