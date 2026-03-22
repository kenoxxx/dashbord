import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap');

        /* Цветовая палитра: Космический минимализм */
        :root {
            --bg-color: #0A0E17;        /* Deep space background */
            --card-bg: rgba(19, 26, 38, 0.7); /* Glassmorphism cards */
            --neon-blue: #00F0FF;       /* Neon accents */
            --neon-purple: #B026FF;     /* Secondary neon */
            --text-main: #E2E8F0;       /* Main readable text */
            --text-muted: #94A3B8;      /* Muted text */
            --border-color: rgba(0, 240, 255, 0.15); /* Subtle borders */
        }
        
        /* Глобальные настройки фона и шрифтов */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Стилизация Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0d121c !important;
            border-right: 1px solid var(--border-color);
        }
        
        /* Моноширинный шрифт для кода и текстовых полей */
        code, pre, .stTextArea textarea {
            font-family: 'Fira Code', 'JetBrains Mono', monospace !important;
            font-size: 0.95em !important;
        }
        
        /* Оформление карточек (Glassmorphism) */
        div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
        }
        
        /* Стилизация полей ввода текста */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid #1E293B !important;
            color: var(--text-main) !important;
            border-radius: 8px !important;
            transition: all 0.2s ease;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
            border-color: var(--neon-blue) !important;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.25) !important;
        }
        
        /* Стилизация кнопок */
        .stButton > button {
            background-color: rgba(19, 26, 38, 0.9);
            border: 1px solid var(--neon-purple);
            color: var(--text-main);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            border-color: var(--neon-blue);
            color: var(--neon-blue);
            box-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
            transform: translateY(-1px);
        }
        
        /* Стилизация заголовков */
        h1, h2, h3 {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em;
        }
        </style>
    """, unsafe_allow_html=True)
