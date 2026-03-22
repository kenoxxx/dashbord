import streamlit as st
from ui.styles import inject_custom_css
from views.library import render_library
from views.constructor import render_constructor
from views.vault import render_vault

# Настройка страницы
st.set_page_config(
    page_title="Prompt Nebula",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация состояния
if 'current_page' not in st.session_state:
    st.session_state.current_page = "📚 Библиотека Промптов"
if 'selected_prompt' not in st.session_state:
    st.session_state.selected_prompt = None

# Инъекция кастомного CSS
inject_custom_css()

def main():
    st.sidebar.title("🌌 Prompt Nebula")
    st.sidebar.markdown("---")
    
    pages = ["📚 Библиотека Промптов", "🛠 Конструктор Шаблонов", "🔐 Секретное Хранилище (Vault)"]
    
    try:
        current_index = pages.index(st.session_state.current_page)
    except ValueError:
        current_index = 0

    page = st.sidebar.radio(
        "Главное меню",
        pages,
        index=current_index,
        key="page_selector"
    )
    
    if st.session_state.current_page != page:
        st.session_state.current_page = page
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.caption("v1.0.0 | Локальный дашборд")
    
    # Роутинг страниц
    if page == "📚 Библиотека Промптов":
        render_library()
    elif page == "🛠 Конструктор Шаблонов":
        render_constructor()
    elif page == "🔐 Секретное Хранилище (Vault)":
        render_vault()

if __name__ == "__main__":
    main()
