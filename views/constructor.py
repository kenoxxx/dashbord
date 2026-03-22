import streamlit as st
import re
from utils.parser import extract_variables, build_prompt, count_tokens

def render_constructor():
    st.title("🛠 Конструктор Шаблонов")
    st.markdown("Заполните переменные выбранного промпта для генерации финального текста.")

    if 'selected_prompt' not in st.session_state or st.session_state.selected_prompt is None:
        st.info("Пожалуйста, сначала выберите промпт из **Библиотеки Промптов**.")
        return

    p = st.session_state.selected_prompt
    st.markdown(f"### ✨ Активный промпт: {p['name']}")
    
    mode = p.get('mode', 'simple')
    if mode == 'simple':
        template = p.get('simple_template', '')
    else:
        template = f"--- System ---\n{p.get('system_prompt', '')}\n\n--- User ---\n{p.get('user_prompt', '')}"
        
    variables = extract_variables(template)
    
    user_inputs = {}
    if not variables:
        st.success("Этот промпт не содержит динамических переменных (вида {{переменная}}).")
    else:
        st.markdown("#### Заполните переменные:")
        for var in variables:
            # Если в названии переменной есть контекст объема, делаем text_area
            if re.search(r'(текст|контент|описание|статья)', var.lower()):
                user_inputs[var] = st.text_area(var.capitalize())
            else:
                user_inputs[var] = st.text_input(var.capitalize())
                
    st.markdown("---")
    
    # Генерация в реальном времени
    final_prompt = build_prompt(template, user_inputs)
    
    st.markdown("### 🚀 Результат:")
    st.code(final_prompt, language='markdown')
    
    tokens = count_tokens(final_prompt)
    st.caption(f"📊 Оценка токенов (~GPT-4o/tiktoken): **{tokens} токенов**")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🚀 COPY RESULT", type="primary"):
            st.toast("Промпт готов! Нажмите иконку копирования в блоке кода выше.", icon="✅")
    with col2:
        st.download_button(
            label="Сохранить как .md файл",
            data=final_prompt.encode('utf-8'),
            file_name=f"{p['name']}_result.md",
            mime="text/markdown"
        )
