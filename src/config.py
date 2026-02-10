from pathlib import Path
import os

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Assets
GIF_PATH = BASE_DIR / "assets" / "jarvis_animation.gif"

# Data folders
DATA_DIR = BASE_DIR / "data"
SAVE_FOLDER = DATA_DIR / "notes"
JARVIS_CHROME_PROFILE_PATH = DATA_DIR / "chrome_profile"

# API Key (OpenRouter)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Model name
AI_MODEL = "gryphe/mythomax-l2-13b"
