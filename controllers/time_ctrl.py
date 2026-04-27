from dataclasses import asdict
from datetime import datetime

from models.project import TimeEntry
from models import storage


def add_entry(
    project_id: int,
    entry_date: str,
    duration_minutes: int,
    notes: str = '',
    entry_type: str = 'manual',
) -> TimeEntry:
    entries = storage.load_entries()
    entry = TimeEntry(
        id=storage.next_id(entries),
        project_id=project_id,
        date=entry_date,
        duration_minutes=duration_minutes,
        notes=notes.strip(),
        entry_type=entry_type,
        created_at=datetime.now().isoformat(),
    )
    entries.append(asdict(entry))
    storage.save_entries(entries)
    return entry


def get_entries(project_id: int | None = None) -> list[TimeEntry]:
    entries = storage.load_entries()
    if project_id is not None:
        entries = [e for e in entries if e['project_id'] == project_id]
    entries_sorted = sorted(entries, key=lambda x: x['created_at'], reverse=True)
    return [TimeEntry(**e) for e in entries_sorted]


def get_summary() -> dict[int, int]:
    """Devuelve {project_id: total_minutes}."""
    summary: dict[int, int] = {}
    for entry in storage.load_entries():
        pid = entry['project_id']
        summary[pid] = summary.get(pid, 0) + entry['duration_minutes']
    return summary


def format_duration(minutes: int) -> str:
    """Convierte minutos a string legible, ej: '2h 30m'."""
    h, m = divmod(minutes, 60)
    if h and m:
        return f"{h}h {m}m"
    if h:
        return f"{h}h"
    return f"{m}m"
