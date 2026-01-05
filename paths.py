from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve().parent
SAVE_DIRECTORY = BASE_DIRECTORY / 'save files'
SAVE_DIRECTORY.mkdir(exist_ok=True)