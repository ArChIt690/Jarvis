import sys
from pathlib import Path

BACKEND_SRC = Path(__file__).parent / "Backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))