import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
PROJECTS_FILE = DATA_DIR / 'projects.json'
ENTRIES_FILE = DATA_DIR / 'entries.json'


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def load_projects() -> list[dict]:
    _ensure_data_dir()
    if not PROJECTS_FILE.exists():
        return []
    return json.loads(PROJECTS_FILE.read_text(encoding='utf-8'))


def save_projects(projects: list[dict]) -> None:
    _ensure_data_dir()
    PROJECTS_FILE.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )


def load_entries() -> list[dict]:
    _ensure_data_dir()
    if not ENTRIES_FILE.exists():
        return []
    return json.loads(ENTRIES_FILE.read_text(encoding='utf-8'))


def save_entries(entries: list[dict]) -> None:
    _ensure_data_dir()
    ENTRIES_FILE.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )


def next_id(items: list[dict]) -> int:
    if not items:
        return 1
    return max(item['id'] for item in items) + 1
