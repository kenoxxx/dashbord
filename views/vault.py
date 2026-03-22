import streamlit as st
import uuid
from utils.vault import init_vault, is_vault_initialized, verify_password, get_credentials, add_credential, delete_credential

def render_vault():
    st.title("🔐 Секретное Хранилище (Vault)")
    st.markdown("Защищенное хранилище API-ключей и паролей. Ваши данные шифруются (Fernet) с использованием Мастер-пароля.")

    if not is_vault_initialized():
        st.warning("Хранилище Vault еще не инициализировано.")
        with st.form("init_vault_form"):
            st.info("Придумайте надежный Мастер-пароль. Он будет использоваться для шифрования всех записей. Восстановить его невозможно!")
            new_pwd = st.text_input("Новый Мастер-пароль", type="password")
            confirm_pwd = st.text_input("Подтвердите пароль", type="password")
            submitted = st.form_submit_button("📁 Создать Vault")
            if submitted:
                if new_pwd != confirm_pwd:
                    st.error("Пароли не совпадают.")
                elif len(new_pwd) < 4:
                    st.error("Пароль слишком короткий.")
                else:
                    init_vault(new_pwd)
                    st.success("Vault успешно создан! Войдите под своим новым паролем.")
                    st.rerun()
        return

    # Авторизация
    if 'vault_unlocked' not in st.session_state or not st.session_state.vault_unlocked:
        with st.form("unlock_vault"):
            pwd = st.text_input("Введите Мастер-пароль", type="password")
            submitted = st.form_submit_button("🔓 Открыть Vault")
            if submitted:
                if verify_password(pwd):
                    st.session_state.vault_unlocked = True
                    st.session_state.vault_pwd = pwd
                    st.rerun()
                else:
                    st.error("Неверный Мастер-пароль.")
        return

    # Vault разблокирован
    st.success("Vault открыт.", icon="🔓")
    if st.button("Закрыть Vault (Lock)🔒"):
        st.session_state.vault_unlocked = False
        st.session_state.vault_pwd = ""
        st.rerun()

    pwd = st.session_state.vault_pwd
    credentials = get_credentials(pwd)

    st.markdown("### Сохраненные доступы")
    if not credentials:
        st.info("Ваш Vault пуст.")
    else:
        for c in credentials:
            with st.expander(f"🔑 {c['service']} ({c['login']})"):
                st.text(f"Логин / Email: {c['login']}")
                st.code(c['password'], language="text")
                if c.get("notes"):
                    st.markdown(f"**Заметки:**\n{c['notes']}")
                
                if st.button("Удалить", key=f"del_cred_{c['id']}", type="primary"):
                    delete_credential(pwd, c['id'])
                    st.rerun()

    st.markdown("### ➕ Добавить запись")
    with st.form("new_cred_form"):
        col1, col2 = st.columns(2)
        with col1:
            i_service = st.text_input("Сервис (например, OpenAI API)")
            i_login = st.text_input("Логин / Email")
        with col2:
            i_pwd = st.text_input("Пароль / Токен", type="password")
            i_notes = st.text_area("Заметки (опционально)")
        
        if st.form_submit_button("Сохранить в Vault"):
            if i_service and i_pwd:
                add_credential(pwd, {
                    "id": str(uuid.uuid4()),
                    "service": i_service,
                    "login": i_login,
                    "password": i_pwd,
                    "notes": i_notes
                })
                st.success("Учетные данные сохранены!")
                st.rerun()
            else:
                st.error("Сервис и Пароль обязательны.")
