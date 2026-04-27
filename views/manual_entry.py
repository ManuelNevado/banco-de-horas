from datetime import date

import streamlit as st

from controllers import project_ctrl, time_ctrl


def render() -> None:
    st.title("Imputar horas")

    projects = project_ctrl.get_projects()
    if not projects:
        st.warning("Crea al menos un proyecto antes de imputar horas.")
        return

    project_names = [p.name for p in projects]
    project_by_name = {p.name: p for p in projects}

    with st.form("form_manual_entry", clear_on_submit=True):
        selected_name = st.selectbox("Proyecto", project_names)
        entry_date = st.date_input("Fecha", value=date.today())

        col_h, col_m = st.columns(2)
        hours = col_h.number_input("Horas", min_value=0, max_value=23, value=0, step=1)
        minutes = col_m.number_input("Minutos", min_value=0, max_value=59, value=0, step=5)

        notes = st.text_area("Notas (opcional)", height=80)
        submitted = st.form_submit_button("Guardar imputacion", type="primary")

    if submitted:
        total_minutes = int(hours) * 60 + int(minutes)
        if total_minutes == 0:
            st.error("La duracion debe ser mayor que 0.")
            return

        project = project_by_name[selected_name]
        time_ctrl.add_entry(
            project_id=project.id,
            entry_date=str(entry_date),
            duration_minutes=total_minutes,
            notes=notes,
            entry_type='manual',
        )
        st.success(
            f"Guardado: {time_ctrl.format_duration(total_minutes)} en '{selected_name}' "
            f"el {entry_date}."
        )
