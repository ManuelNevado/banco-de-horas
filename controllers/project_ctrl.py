from dataclasses import asdict
from datetime import datetime

from models.project import Project
from models import storage


def get_projects() -> list[Project]:
    return [Project(**p) for p in storage.load_projects()]


def create_project(name: str, description: str = '', color: str = '#4A90D9') -> Project:
    projects = storage.load_projects()
    if any(p['name'].lower() == name.lower() for p in projects):
        raise ValueError(f"Ya existe un proyecto con el nombre '{name}'")
    project = Project(
        id=storage.next_id(projects),
        name=name.strip(),
        description=description.strip(),
        color=color,
        created_at=datetime.now().isoformat(),
    )
    projects.append(asdict(project))
    storage.save_projects(projects)
    return project


def delete_project(project_id: int) -> None:
    projects = [p for p in storage.load_projects() if p['id'] != project_id]
    storage.save_projects(projects)
    entries = [e for e in storage.load_entries() if e['project_id'] != project_id]
    storage.save_entries(entries)
