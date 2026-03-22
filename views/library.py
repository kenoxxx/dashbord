import streamlit as st
import uuid
from utils.storage import get_prompts, get_categories, get_tags, add_prompt, delete_prompt

def render_library():
    st.title("📚 Библиотека Промптов")
    st.markdown("Здесь хранятся ваши атомарные промпты и шаблоны.")

    prompts = get_prompts()
    categories = get_categories()
    tags = get_tags()

    # Блок фильтрации
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_q = st.text_input("Поиск по названию", placeholder="Введите название промпта...")
    with col2:
        filter_cat = st.selectbox("Категория", ["Все"] + categories)
    with col3:
        filter_tag = st.multiselect("Теги", tags)

    # Применение фильтров
    filtered_prompts = prompts
    if search_q:
        filtered_prompts = [p for p in filtered_prompts if search_q.lower() in p.get("name", "").lower()]
    if filter_cat != "Все":
        filtered_prompts = [p for p in filtered_prompts if p.get("category") == filter_cat]
    if filter_tag:
        filtered_prompts = [p for p in filtered_prompts if any(t in p.get("tags", []) for t in filter_tag)]

    st.markdown("---")

    # Отображение списка
    if not filtered_prompts:
        st.info("Промпты не найдены. Создайте новый!")
    else:
        for p in filtered_prompts:
            with st.expander(f"✨ {p['name']} | 📁 {p['category']}"):
                tags_str = ", ".join(p.get('tags', []))
                if tags_str:
                    st.caption(f"🔖 Теги: {tags_str}")
                
                mode = p.get('mode', 'simple')
                
                if mode == 'simple':
                    st.markdown("**Шаблон:**")
                    st.code(p.get('simple_template', ''), language='markdown')
                else:
                    st.markdown("**System Prompt:**")
                    st.code(p.get('system_prompt', ''), language='markdown')
                    st.markdown("**User Prompt:**")
                    st.code(p.get('user_prompt', ''), language='markdown')
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
                with col_btn1:
                    if st.button("Использовать", key=f"use_{p['id']}"):
                        st.session_state.selected_prompt = p
                        st.session_state.current_page = "🛠 Конструктор Шаблонов"
                        st.rerun()
                with col_btn2:
                    if st.button("Удалить", key=f"del_{p['id']}", type="primary"):
                        delete_prompt(p['id'])
                        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### ➕ Добавить новый промпт")
    with st.container():
        with st.form("new_prompt_form"):
            new_name = st.text_input("Название промпта")
            new_cat = st.selectbox("Категория", categories)
            new_tags = st.multiselect("Теги", tags)
            new_mode = st.radio("Режим", ["Simple", "System/User"], horizontal=True)
            
            new_simple = ""
            new_sys = ""
            new_user = ""
            
            if new_mode == "Simple":
                new_simple = st.text_area("Текст шаблона", placeholder="Введите текст. Для переменных используйте {{имя}}.")
            else:
                new_sys = st.text_area("System Prompt", placeholder="Инструкции для системы...")
                new_user = st.text_area("User Prompt", placeholder="Шаблон для пользователя. Переменные {{...}}.")

            submitted = st.form_submit_button("Сохранить промпт")
            if submitted:
                if new_name.strip() == "":
                    st.error("Название не может быть пустым.")
                else:
                    new_prompt = {
                        "id": str(uuid.uuid4()),
                        "name": new_name,
                        "category": new_cat,
                        "tags": new_tags,
                        "mode": "simple" if new_mode == "Simple" else "system_user",
                        "simple_template": new_simple,
                        "system_prompt": new_sys,
                        "user_prompt": new_user
                    }
                    add_prompt(new_prompt)
                    st.success("Промпт успешно добавлен!")
                    st.rerun()
