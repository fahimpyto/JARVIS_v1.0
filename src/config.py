from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

GIF_PATH = BASE_DIR / "assets" / "jarvis_animation.gif"

DATA_DIR = BASE_DIR / "data"
SAVE_FOLDER = DATA_DIR / "notes"
JARVIS_CHROME_PROFILE_PATH = DATA_DIR / "chrome_profile"

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
AI_MODEL = "gryphe/mythomax-l2-13b"
