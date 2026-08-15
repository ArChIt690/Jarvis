from pathlib import Path
import sys
from config.settings import MEMORY_DIR

def path_conn():
    path = MEMORY_DIR / "profile.md"
    if not path.exists():
        return ""
    return path.read_text(encoding = "utf-8")


