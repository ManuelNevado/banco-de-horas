from datetime import date, datetime

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from controllers import project_ctrl, time_ctrl


def render() -> None:
    st.title("Timer")

    projects = project_ctrl.get_projects()
    if not projects:
        st.warning("Crea al menos un proyecto antes de usar el timer.")
        return

    # Refresco automatico cada segundo solo mientras el timer corre
    if st.session_state.get('timer_running'):
        st_autorefresh(interval=1000, key="timer_refresh")

    project_names = [p.name for p in projects]
    project_by_name = {p.name: p for p in projects}

    # Selector de proyecto (bloqueado mientras el timer corre)
    timer_running = st.session_state.get('timer_running', False)

    selected_name = st.selectbox(
        "Proyecto",
        project_names,
        disabled=timer_running,
        key="timer_project_name",
    )

    st.divider()

    # Display del tiempo transcurrido
    if timer_running:
        elapsed = datetime.now() - st.session_state['timer_start']
        total_seconds = int(elapsed.total_seconds())
        h, remainder = divmod(total_seconds, 3600)
        m, s = divmod(remainder, 60)
        time_display = f"{h:02d}:{m:02d}:{s:02d}"

        proj_name = st.session_state.get('timer_project_name_saved', selected_name)
        st.markdown(
            f"<div style='text-align:center'>"
            f"<p style='color:gray;margin-bottom:4px'>Registrando en: <b>{proj_name}</b></p>"
            f"<span style='font-size:4rem;font-weight:700;letter-spacing:4px'>"
            f"{time_display}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='text-align:center'>"
            "<span style='font-size:4rem;font-weight:700;letter-spacing:4px;color:#bbb'>"
            "00:00:00</span>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.write("")  # espacio

    # Botones Iniciar / Detener
    col_l, col_btn, col_r = st.columns([1, 1, 1])
    with col_btn:
        if not timer_running:
            if st.button("Iniciar", type="primary", use_container_width=True):
                st.session_state['timer_running'] = True
                st.session_state['timer_start'] = datetime.now()
                st.session_state['timer_project_name_saved'] = selected_name
                st.rerun()
        else:
            if st.button("Detener", type="secondary", use_container_width=True):
                elapsed = datetime.now() - st.session_state['timer_start']
                duration_minutes = max(1, int(elapsed.total_seconds() / 60))

                proj_name = st.session_state.get('timer_project_name_saved', selected_name)
                project = project_by_name.get(proj_name)

                if project:
                    time_ctrl.add_entry(
                        project_id=project.id,
                        entry_date=str(date.today()),
                        duration_minutes=duration_minutes,
                        entry_type='timer',
                    )
                    saved_duration = time_ctrl.format_duration(duration_minutes)

                # Limpiar estado del timer
                for key in ('timer_running', 'timer_start', 'timer_project_name_saved'):
                    st.session_state.pop(key, None)

                if project:
                    st.success(f"Guardado: {saved_duration} en '{proj_name}'.")
                st.rerun()

    # Nota informativa
    if timer_running:
        st.caption("El timer sigue corriendo si cambias de seccion.")
