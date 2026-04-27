from dataclasses import dataclass, field


@dataclass
class Project:
    name: str
    description: str = ''
    color: str = '#4A90D9'
    created_at: str = ''
    id: int | None = None


@dataclass
class TimeEntry:
    project_id: int
    date: str               # YYYY-MM-DD
    duration_minutes: int
    entry_type: str         # 'manual' | 'timer'
    notes: str = ''
    created_at: str = ''
    id: int | None = None
