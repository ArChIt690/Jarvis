import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

ROOT_TEMP = os.getenv("JARVIS_ROOT")
if ROOT_TEMP is None:
    raise ValueError("JARVIS_ROOT directory path in environment variable is not set.")
ROOT = Path(ROOT_TEMP)
if not ROOT.exists():
    raise ValueError(f"JARVIS_ROOT directory path {ROOT} does not exist.")

MEMORY_DIR = ROOT/"memory"
LESSONS_DIR = ROOT/"lessons"
SKILLS_DIR = ROOT/"skills"
HANDOFFS_DIR = ROOT/"handoffs"
LOGS_DIR = ROOT/"logs"
STATE_DIR = ROOT/"state"
EVALS_DIR = ROOT/"evals"
CHECKPOINT_DB = STATE_DIR/ "checkpoints.sqlite"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX"))