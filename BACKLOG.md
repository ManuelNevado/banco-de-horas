# BACKLOG — Banco de Horas

## Visión del producto

Aplicación local minimalista para que un desarrollador individual registre el tiempo que dedica a sus proyectos personales, con imputación manual y timer en vivo.

---

## Sprint 1 — POC ✅ COMPLETADO

**Objetivo**: Aplicación funcional end-to-end con las dos formas de imputar horas y un dashboard básico.

**Criterio de éxito**: Se puede crear un proyecto, imputar horas manuales, usar el timer y ver el resumen — todo sin errores.

---

### US-01 — Gestión de proyectos ✅

**Como** usuario, **quiero** crear y eliminar proyectos con nombre y descripción **para** poder organizar mis imputaciones por proyecto.

**Acceptance criteria**:
- [x] Se puede crear un proyecto con nombre (obligatorio), descripción (opcional) y color.
- [x] Los proyectos se listan en el dashboard.
- [x] Se puede eliminar un proyecto (con sus imputaciones asociadas).
- [x] No se pueden crear dos proyectos con el mismo nombre.

**Tareas técnicas**:
- [x] Definir dataclass `Project` en `models/project.py`
- [x] Implementar storage JSON en `models/storage.py`
- [x] Implementar `create_project()`, `get_projects()`, `delete_project()` en `project_ctrl.py`
- [x] Añadir formulario "Nuevo proyecto" en `views/dashboard.py`

---

### US-02 — Imputación manual de horas ✅

**Como** usuario, **quiero** registrar manualmente horas y minutos en un proyecto para una fecha **para** anotar trabajo ya realizado.

**Acceptance criteria**:
- [x] Se puede seleccionar proyecto, fecha, horas (0–23) y minutos (0–59).
- [x] Campo opcional de notas.
- [x] La entrada se guarda y aparece en el dashboard.
- [x] No se puede guardar una entrada con 0 horas y 0 minutos.

**Tareas técnicas**:
- [x] Definir dataclass `TimeEntry` en `models/project.py`
- [x] Implementar `add_entry()` y `get_entries()` en `time_ctrl.py`
- [x] Implementar vista `views/manual_entry.py`

---

### US-03 — Timer en vivo ✅

**Como** usuario, **quiero** iniciar un contador que se actualice en tiempo real y detenerlo para guardar las horas **para** registrar tiempo mientras trabajo.

**Acceptance criteria**:
- [x] Botón "Iniciar" arranca el contador visible (HH:MM:SS).
- [x] El contador se actualiza cada segundo sin que el usuario haga nada.
- [x] Botón "Detener" para el contador y guarda la entrada en el proyecto seleccionado.
- [x] Solo puede haber un timer activo a la vez.
- [x] Si el usuario cambia de vista y vuelve, el timer sigue corriendo.
- [x] El tiempo mínimo registrado es 1 minuto (redondeo hacia arriba o mínimo 1).

**Tareas técnicas**:
- [x] Implementar vista `views/timer_view.py`
- [x] Integrar `streamlit-autorefresh` para el refresco de 1 segundo
- [x] Gestionar `st.session_state` para `timer_running`, `timer_start`, `timer_project_name_saved`
- [x] Al detener: calcular minutos y llamar a `time_ctrl.add_entry(entry_type='timer')`

---

### US-04 — Dashboard de resumen ✅

**Como** usuario, **quiero** ver un resumen de las horas totales por proyecto y las últimas imputaciones **para** tener visión global de mi tiempo.

**Acceptance criteria**:
- [x] Métricas: total de horas registradas (global), nº de proyectos y nº de imputaciones.
- [x] Tabla con las últimas 10 imputaciones (proyecto, fecha, duración, tipo, notas).
- [x] Si no hay proyectos, muestra un mensaje de bienvenida con instrucciones.

**Tareas técnicas**:
- [x] Implementar `get_summary()` y `format_duration()` en `time_ctrl.py`
- [x] Implementar `views/dashboard.py` con `st.metric`, `st.dataframe`

---

### US-05 — Infraestructura base ✅

**Tareas técnicas transversales**:
- [x] Estructura de directorios y módulos `__init__.py`
- [x] `README.md`, `DEVELOPER.md`, `CLAUDE.md`, `BACKLOG.md`
- [x] `requirements.txt` con dependencias (`streamlit`, `streamlit-autorefresh`)
- [x] `.gitignore` (excluye `data/`, `.venv/`, `__pycache__/`)
- [x] `app.py` con sidebar de navegación, routing y indicador de timer activo
- [x] `models/storage.py` con load/save JSON y generación de IDs

---

## Sprints futuros (backlog de producto)

Estas ideas quedan fuera de la POC pero son candidatas para iteraciones siguientes:

| Idea | Prioridad estimada |
|---|---|
| Editar imputaciones existentes | Media |
| Filtrar dashboard por rango de fechas | Media |
| Gráfico de horas por semana/mes (Plotly/Altair) | Baja |
| Exportar imputaciones a CSV | Baja |
| Múltiples timers simultáneos | Baja |
| Tags/etiquetas en imputaciones | Baja |
| Vista semanal tipo timesheet | Baja |

---

## Registro de sesiones

| Fecha | Estado al cerrar |
|---|---|
| 2026-04-27 | Documentación inicial completada. Sprint 1 planificado. Sin código implementado. |
| 2026-04-27 | Sprint 1 completado. POC funcional: app.py, models, controllers, views implementados. Persistencia en JSON. |
