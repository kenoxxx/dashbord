import json
import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VAULT_FILE = DATA_DIR / "vault.json.enc"
SALT_FILE = DATA_DIR / "vault.salt"

def _get_key_from_password(password: str, salt: bytes) -> bytes:
    """Генерирует криптографический ключ на основе пароля пользователя."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def init_vault(password: str):
    """Инициализирует хранилище Vault с использованием мастер-пароля."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
        
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
        
    key = _get_key_from_password(password, salt)
    f_obj = Fernet(key)
    
    empty_data = json.dumps({"credentials": []}).encode()
    encrypted_data = f_obj.encrypt(empty_data)
    
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)

def is_vault_initialized() -> bool:
    """Проверяет, было ли уже инициализировано хранилище Vault."""
    return VAULT_FILE.exists() and SALT_FILE.exists()

def verify_password(password: str) -> bool:
    """Проверяет мастер-пароль, пытаясь дешифровать Vault."""
    if not is_vault_initialized():
        return False
        
    try:
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
            
        key = _get_key_from_password(password, salt)
        f_obj = Fernet(key)
        
        with open(VAULT_FILE, "rb") as f:
            encrypted_data = f.read()
            
        f_obj.decrypt(encrypted_data)
        return True
    except Exception:
        return False

def load_vault(password: str) -> dict:
    """Загружает расшифрованные данные Vault."""
    if not verify_password(password):
        raise ValueError("Неверный Мастер-пароль")
        
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
        
    key = _get_key_from_password(password, salt)
    f_obj = Fernet(key)
    
    with open(VAULT_FILE, "rb") as f:
        encrypted_data = f.read()
    
    decrypted_data = f_obj.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())

def save_vault(password: str, data: dict):
    """Сохраняет и шифрует данные Vault."""
    if not verify_password(password):
        raise ValueError("Неверный Мастер-пароль")
        
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
        
    key = _get_key_from_password(password, salt)
    f_obj = Fernet(key)
    
    json_bytes = json.dumps(data, ensure_ascii=False).encode()
    encrypted_data = f_obj.encrypt(json_bytes)
    
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)

# CRUD операции для Vault
def get_credentials(password: str):
    data = load_vault(password)
    return data.get("credentials", [])

def add_credential(password: str, cred_data: dict):
    """
    cred_data должно содержать ключи:
    id (str), service (str), login (str), password (str), notes (str)
    """
    data = load_vault(password)
    data.setdefault("credentials", []).append(cred_data)
    save_vault(password, data)
    
def delete_credential(password: str, cred_id: str):
    data = load_vault(password)
    credentials = data.get("credentials", [])
    data["credentials"] = [c for c in credentials if c.get("id") != cred_id]
    save_vault(password, data)
