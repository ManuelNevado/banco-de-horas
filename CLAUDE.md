# CLAUDE.md — Contexto de proyecto para sesiones de Claude Code

Este archivo permite recuperar el contexto completo del proyecto al inicio de una nueva sesión.

---

## Identidad del proyecto

**Nombre**: Banco de Horas  
**Stack**: Python 3.11+, Streamlit, SQLite (`sqlite3` estándar)  
**Patrón**: MVC adaptado a Streamlit  
**Estado actual**: POC en planificación / inicio de desarrollo  

---

## Arquitectura de decisiones clave (ADRs)

### ADR-1: Persistencia en JSON
Se usan dos ficheros JSON en `data/`: `projects.json` y `entries.json`.  
**Motivo**: POC personal con volumen pequeño. Sin base de datos, sin servidor, sin ORM. Ficheros legibles y editables a mano. Gestionados por `models/storage.py`.

### ADR-2: MVC adaptado a Streamlit
Streamlit rerenderiza el script completo en cada interacción (no tiene ciclo de vida de controller clásico).  
- `models/` — solo Python puro, cero imports de Streamlit.  
- `controllers/` — solo Python puro, cero imports de Streamlit.  
- `views/` — todo Streamlit. Llama a controllers. Gestiona `st.session_state`.

### ADR-3: Timer con streamlit-autorefresh
El contador en vivo usa el componente `streamlit-autorefresh` para refrescar la UI sin bloquear el hilo principal.  
El tiempo de inicio del timer se guarda en `st.session_state['timer_start']`.

### ADR-4: Persistencia del timer en DB
Cuando el timer se detiene, la entrada se escribe en SQLite como cualquier otra imputación manual.  
El timer activo **no** se persiste en DB — solo vive en `session_state` (la sesión de Streamlit).

---

## Estructura de ficheros

```
banco-de-horas/
├── app.py                  # Entry point. Sidebar de navegación + routing a vistas.
├── models/
│   ├── __init__.py
│   ├── project.py          # Dataclass Project, Dataclass TimeEntry
│   └── storage.py          # load/save JSON para projects y entries
├── controllers/
│   ├── __init__.py
│   ├── project_ctrl.py     # get_projects(), create_project(), delete_project()
│   └── time_ctrl.py        # add_entry(), get_entries(), get_summary()
├── views/
│   ├── __init__.py
│   ├── dashboard.py        # Resumen de horas por proyecto (tabla + métricas)
│   ├── manual_entry.py     # Formulario: proyecto, fecha, horas, minutos, notas
│   └── timer_view.py       # Contador en vivo con autorefresh
├── BACKLOG.md              # Sprint planning y user stories
├── CLAUDE.md               # Este archivo
├── README.md               # Documentación de usuario
├── DEVELOPER.md            # Documentación técnica para desarrolladores
└── requirements.txt
```

---

## Modelos de datos

### Project
```python
@dataclass
class Project:
    id: int | None
    name: str
    description: str
    color: str          # hex color para la UI
    created_at: str     # ISO 8601
```

### TimeEntry
```python
@dataclass
class TimeEntry:
    id: int | None
    project_id: int
    date: str           # ISO 8601 date (YYYY-MM-DD)
    duration_minutes: int
    notes: str
    entry_type: str     # 'manual' | 'timer'
    created_at: str     # ISO 8601 datetime
```

---

## Estado actual del proyecto

- [x] Documentación inicial (README, DEVELOPER, BACKLOG, CLAUDE.md)
- [x] Sprint 1 — POC implementada (app.py, models, controllers, views)

---

## Cómo retomar el trabajo en una nueva sesión

1. Leer este archivo (`CLAUDE.md`) y `BACKLOG.md` para entender el estado.
2. Verificar qué tareas del Sprint 1 están marcadas como completadas en `BACKLOG.md`.
3. Leer el código existente antes de modificar nada (`app.py`, luego los módulos relevantes).
4. Seguir las convenciones de ADRs de este archivo. No introducir ORM ni dependencias nuevas sin discutirlo.

---

## Convenciones de código

- **Formato**: Black, line-length 88.
- **Tipos**: Type hints en todas las funciones de `models/` y `controllers/`. Opcional en `views/`.
- **Strings**: f-strings. No `.format()`.
- **DB**: Siempre usar parámetros `?` en queries SQL. Nunca concatenar strings con datos de usuario.
- **Commits**: Convención `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.

---

## Comandos útiles de sesión

```bash
# Instalar dependencias
pip install -r requirements.txt

# Arrancar la app
streamlit run app.py

# Limpiar DB de desarrollo (reset)
rm banco_horas.db
```

---

## Persona del usuario

Manuel — desarrollador con criterio técnico que quiere mantener la solución simple y pragmática.  
Prefiere no añadir complejidad innecesaria. La POC debe ser funcional antes que perfecta.
