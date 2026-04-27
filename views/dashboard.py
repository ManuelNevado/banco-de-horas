import streamlit as st

from controllers import project_ctrl, time_ctrl


def render() -> None:
    st.title("Dashboard")

    projects = project_ctrl.get_projects()
    project_map = {p.id: p for p in projects}

    if not projects:
        st.info("No tienes proyectos todavia. Crea uno para empezar.")
        _new_project_form()
        return

    # ── Metricas globales ──────────────────────────────────────────────────
    summary = time_ctrl.get_summary()
    total_minutes = sum(summary.values())
    total_entries = len(time_ctrl.get_entries())

    col1, col2, col3 = st.columns(3)
    col1.metric("Tiempo total", time_ctrl.format_duration(total_minutes))
    col2.metric("Proyectos", len(projects))
    col3.metric("Imputaciones", total_entries)

    st.divider()

    # ── Tabla de proyectos ─────────────────────────────────────────────────
    st.subheader("Proyectos")

    for project in projects:
        minutes = summary.get(project.id, 0)
        col_color, col_name, col_hours, col_del = st.columns([0.05, 0.55, 0.25, 0.15])

        col_color.markdown(
            f"<div style='background:{project.color};width:18px;height:18px;"
            f"border-radius:4px;margin-top:6px'></div>",
            unsafe_allow_html=True,
        )
        col_name.markdown(f"**{project.name}**  \n{project.description or ''}")
        col_hours.markdown(
            f"<span style='font-size:1.1rem;font-weight:600'>"
            f"{time_ctrl.format_duration(minutes)}</span>",
            unsafe_allow_html=True,
        )
        if col_del.button("Borrar", key=f"del_{project.id}", type="secondary"):
            project_ctrl.delete_project(project.id)
            st.rerun()

    st.divider()

    # ── Ultimas imputaciones ───────────────────────────────────────────────
    st.subheader("Ultimas imputaciones")
    entries = time_ctrl.get_entries()[:10]

    if not entries:
        st.caption("Aun no hay imputaciones.")
    else:
        rows = []
        for e in entries:
            proj = project_map.get(e.project_id)
            rows.append({
                "Proyecto": proj.name if proj else "—",
                "Fecha": e.date,
                "Duracion": time_ctrl.format_duration(e.duration_minutes),
                "Tipo": "Manual" if e.entry_type == "manual" else "Timer",
                "Notas": e.notes or "—",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)

    st.divider()

    # ── Nuevo proyecto ─────────────────────────────────────────────────────
    with st.expander("Nuevo proyecto"):
        _new_project_form()


def _new_project_form() -> None:
    with st.form("form_new_project", clear_on_submit=True):
        name = st.text_input("Nombre *")
        description = st.text_input("Descripcion")
        color = st.color_picker("Color", value="#4A90D9")
        submitted = st.form_submit_button("Crear proyecto")

    if submitted:
        if not name.strip():
            st.error("El nombre es obligatorio.")
            return
        try:
            project_ctrl.create_project(name, description, color)
            st.success(f"Proyecto '{name}' creado.")
            st.rerun()
        except ValueError as e:
            st.error(str(e))
