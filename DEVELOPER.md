# DEVELOPER.md — Documentación técnica

Guía para entender, extender y mantener el código base de Banco de Horas.

---

## Stack tecnológico

| Componente | Tecnología | Motivo |
|---|---|---|
| UI / Framework | Streamlit | Rápido de iterar, cero HTML/CSS manual |
| Timer en vivo | streamlit-autorefresh | Refresco periódico sin bloquear el hilo |
| Persistencia | JSON (`json` stdlib) | Cero dependencias, legible a mano, suficiente para uso personal |
| Lenguaje | Python 3.11+ | Type hints modernos, dataclasses |

---

## Patrón MVC adaptado a Streamlit

Streamlit es **reactivo y sin estado del servidor**: rerenderiza el script completo en cada interacción del usuario. Esto impide un controller clásico con ciclo de vida propio. La adaptación es:

```
┌─────────────────────────────────────────────┐
│                  app.py                      │
│         (routing + sidebar nav)              │
└──────────────┬──────────────────────────────┘
               │ llama a
       ┌───────▼────────┐
       │    views/      │  ← Streamlit puro
       │  dashboard.py  │     gestiona session_state
       │  manual_entry  │     llama a controllers
       │  timer_view    │
       └───────┬────────┘
               │ llama a
       ┌───────▼────────┐
       │  controllers/  │  ← Python puro, sin Streamlit
       │  project_ctrl  │     recibe datos, aplica lógica
       │  time_ctrl     │     devuelve resultados
       └───────┬────────┘
               │ usa
       ┌───────▼────────┐
       │    models/     │  ← Python puro, sin Streamlit
       │   project.py   │     dataclasses
       │   storage.py   │     lectura/escritura JSON
       └────────────────┘
```

**Regla de oro**: `models/` y `controllers/` no importan `streamlit`. Solo `views/` y `app.py` lo hacen.

---

## Estructura de ficheros detallada

```
banco-de-horas/
├── app.py
│     Entry point de Streamlit. Configura la página, renderiza
│     la sidebar con la navegación y despacha a la vista activa.
│     Muestra indicador "● Timer activo" en sidebar si hay timer corriendo.
│
├── models/
│   ├── __init__.py
│   ├── project.py
│   │     Dataclasses: Project, TimeEntry.
│   │     Sin lógica de negocio, solo estructura de datos.
│   └── storage.py
│         load_projects() / save_projects()  — lee/escribe data/projects.json
│         load_entries()  / save_entries()   — lee/escribe data/entries.json
│         next_id(items)                     — genera el siguiente ID autoincremental
│
├── controllers/
│   ├── __init__.py
│   ├── project_ctrl.py
│   │     get_projects()                        → list[Project]
│   │     create_project(name, desc, color)     → Project
│   │     delete_project(project_id)            → None  (borra también sus entradas)
│   └── time_ctrl.py
│         add_entry(project_id, date, minutes, notes, entry_type) → TimeEntry
│         get_entries(project_id?)              → list[TimeEntry]  (orden: más reciente primero)
│         get_summary()                         → dict[int, int]  (project_id → total_minutes)
│         format_duration(minutes)              → str  (ej: "2h 30m")
│
├── views/
│   ├── __init__.py
│   ├── dashboard.py
│   │     Métricas globales (tiempo total, nº proyectos, nº imputaciones).
│   │     Tabla de proyectos con color, nombre y horas totales.
│   │     Botón de borrar por proyecto.
│   │     Últimas 10 imputaciones en st.dataframe.
│   │     Expander "Nuevo proyecto" con formulario.
│   ├── manual_entry.py
│   │     Formulario con st.form: selectbox proyecto, date_input,
│   │     number_input horas/minutos (columnas), text_area notas.
│   │     Validación: duración > 0.
│   └── timer_view.py
│         Selectbox proyecto (deshabilitado mientras corre el timer).
│         Display HH:MM:SS centrado con HTML inline.
│         Botón Iniciar / Detener (mismo botón, estado alternado).
│         Autorefresh cada 1s solo cuando timer_running es True.
│         Al detener: guarda con entry_type='timer', mínimo 1 minuto.
│
├── data/                   ← creada automáticamente, excluida de git
│   ├── projects.json
│   └── entries.json
│
├── BACKLOG.md
├── CLAUDE.md
├── README.md
├── DEVELOPER.md
└── requirements.txt
```

---

## Modelos de datos

### Dataclasses Python (`models/project.py`)

```python
@dataclass
class Project:
    name: str
    description: str = ''
    color: str = '#4A90D9'
    created_at: str = ''      # ISO 8601 datetime
    id: int | None = None

@dataclass
class TimeEntry:
    project_id: int
    date: str                 # YYYY-MM-DD
    duration_minutes: int
    entry_type: str           # 'manual' | 'timer'
    notes: str = ''
    created_at: str = ''      # ISO 8601 datetime
    id: int | None = None
```

### Estructura JSON en disco

`data/projects.json`:
```json
[
  {
    "id": 1,
    "name": "Mi proyecto",
    "description": "Descripcion opcional",
    "color": "#4A90D9",
    "created_at": "2026-04-27T10:00:00.000000"
  }
]
```

`data/entries.json`:
```json
[
  {
    "id": 1,
    "project_id": 1,
    "date": "2026-04-27",
    "duration_minutes": 90,
    "entry_type": "manual",
    "notes": "Sesion de trabajo",
    "created_at": "2026-04-27T11:30:00.000000"
  }
]
```

---

## Gestión del timer

El timer vive exclusivamente en `st.session_state`. No se persiste en disco mientras está activo — solo al detenerlo.

```python
# Claves usadas en session_state
st.session_state['timer_running']            # bool: True si el timer está corriendo
st.session_state['timer_start']              # datetime: momento de inicio
st.session_state['timer_project_name_saved'] # str: nombre del proyecto seleccionado al iniciar
```

Flujo completo:

```python
# Al pulsar Iniciar
st.session_state['timer_running'] = True
st.session_state['timer_start'] = datetime.now()
st.session_state['timer_project_name_saved'] = selected_name

# Refresco automático (solo activo cuando timer_running es True)
if st.session_state.get('timer_running'):
    st_autorefresh(interval=1000, key="timer_refresh")

# Al pulsar Detener
elapsed = datetime.now() - st.session_state['timer_start']
duration_minutes = max(1, int(elapsed.total_seconds() / 60))
time_ctrl.add_entry(project_id, str(date.today()), duration_minutes, entry_type='timer')

for key in ('timer_running', 'timer_start', 'timer_project_name_saved'):
    st.session_state.pop(key, None)
```

El indicador "● Timer activo" en la sidebar se renderiza en `app.py` comprobando `st.session_state.get('timer_running')`.

---

## Convenciones

### Código
- Type hints en todas las funciones de `models/` y `controllers/`.
- f-strings. No `.format()`.
- `dataclasses.asdict()` para serializar a dict antes de guardar en JSON.

### Commits
Convención [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add timer stop confirmation dialog
fix: timer minutes calculation off-by-one
docs: update DEVELOPER.md
refactor: extract format_duration to time_ctrl
chore: add data/ to .gitignore
```

### Añadir una nueva vista
1. Crear `views/nueva_vista.py` con una función `render()`.
2. Añadir la clave en el dict `PAGES` de `app.py`.
3. Si necesita lógica nueva, añadirla al controller correspondiente (o crear uno nuevo en `controllers/`).

---

## Persistencia JSON — notas operativas

- La carpeta `data/` se crea automáticamente al primer uso mediante `storage._ensure_data_dir()`.
- Para empezar de cero: borrar `data/projects.json` y `data/entries.json`.
- Borrar un proyecto elimina también todas sus imputaciones (lógica en `project_ctrl.delete_project`).
- No hay migraciones de schema. Si cambia la estructura de los dataclasses, los ficheros existentes pueden necesitar ajuste manual o borrado.
- `data/` está excluida de git en `.gitignore` para no versionar datos personales.

---

## Testing (pendiente para post-POC)

Los controllers son Python puro y testables con `pytest`. Para aislar el storage, se puede parchear `models.storage` con `tmp_path` de pytest:

```python
import pytest
from unittest.mock import patch

def test_create_project(tmp_path, monkeypatch):
    monkeypatch.setattr('models.storage.DATA_DIR', tmp_path)
    monkeypatch.setattr('models.storage.PROJECTS_FILE', tmp_path / 'projects.json')
    monkeypatch.setattr('models.storage.ENTRIES_FILE', tmp_path / 'entries.json')

    from controllers.project_ctrl import create_project, get_projects
    create_project('Test', 'desc', '#ff0000')
    projects = get_projects()
    assert len(projects) == 1
    assert projects[0].name == 'Test'
```

Las vistas de Streamlit se pueden testear con `streamlit.testing.v1.AppTest` (disponible desde Streamlit 1.28).
