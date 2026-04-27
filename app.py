import streamlit as st

from views import dashboard, manual_entry, timer_view

st.set_page_config(
    page_title="Banco de Horas",
    page_icon="⏱",
    layout="wide",
)

PAGES = {
    "Dashboard": dashboard,
    "Imputar horas": manual_entry,
    "Timer": timer_view,
}

with st.sidebar:
    st.title("Banco de Horas")
    st.write("")

    # Indicador visual si hay timer activo
    if st.session_state.get('timer_running'):
        st.markdown(
            "<span style='color:#ff4b4b;font-weight:600'>● Timer activo</span>",
            unsafe_allow_html=True,
        )
        st.write("")

    selection = st.radio("Navegacion", list(PAGES.keys()), label_visibility="collapsed")

PAGES[selection].render()
