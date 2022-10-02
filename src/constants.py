"""Модуль настроек парсера."""
from pathlib import Path

MAIN_DOC_URL = "https://docs.python.org/3/"
PEP = "https://peps.python.org/"
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
ARGUMENT_PRETTY = "pretty"
ARGUMENT_FILE = "file"
DOWNLOADS_URL = f"{MAIN_DOC_URL}/download.html"
WHATS_NEW_URL = f"{MAIN_DOC_URL}/whatsnew/"
EXPECTED_STATUS = {
    "A": ["Active", "Accepted"],
    "D": ["Deferred"],
    "F": ["Final"],
    "P": ["Provisional"],
    "R": ["Rejected"],
    "S": ["Superseded"],
    "W": ["Withdrawn"],
    "": ["Draft", "Active"],
}
