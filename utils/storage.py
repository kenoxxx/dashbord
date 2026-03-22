import json
import os
from pathlib import Path

# Базовые директории
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_FILE = DATA_DIR / "prompts.json"

DEFAULT_CATEGORIES = [
    "🤖 Разработка AI",
    "📝 Написание текстов",
    "📊 Аналитика Данных",
    "🎯 Маркетинг",
    "📱 Контент для соцсетей"
]

DEFAULT_TAGS = [
    "AIDA", "PAS", "One-shot", "Few-shot", "Chain-of-Thought", 
    "B2B", "B2C", "Tone: Formal", "Tone: Creative"
]

def init_storage():
    """Создает директорию data и начальный файл prompts.json при их отсутствии."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
        
    if not PROMPTS_FILE.exists():
        default_data = {
            "categories": DEFAULT_CATEGORIES,
            "tags": DEFAULT_TAGS,
            "prompts": []
        }
        with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)

def load_data() -> dict:
    """Загружает все данные из prompts.json."""
    if not PROMPTS_FILE.exists():
        init_storage()
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict):
    """Сохраняет данные в prompts.json."""
    with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# CRUD Список Базовых Элементов
def get_categories():
    return load_data().get("categories", [])

def get_tags():
    return load_data().get("tags", [])

def add_category(category_name: str):
    data = load_data()
    if category_name not in data.get("categories", []):
        data.setdefault("categories", []).append(category_name)
        save_data(data)

def add_tag(tag_name: str):
    data = load_data()
    if tag_name not in data.get("tags", []):
        data.setdefault("tags", []).append(tag_name)
        save_data(data)

# CRUD для Промптов
def get_prompts():
    return load_data().get("prompts", [])

def add_prompt(prompt_data: dict):
    """
    prompt_data должно содержать ключи:
    id (str), name (str), category (str), tags (list), 
    mode (str: 'simple'|'system_user'), 
    simple_template (str), system_prompt (str), user_prompt (str)
    """
    data = load_data()
    data.setdefault("prompts", []).append(prompt_data)
    save_data(data)

def update_prompt(prompt_id: str, updated_data: dict):
    data = load_data()
    prompts = data.get("prompts", [])
    for i, p in enumerate(prompts):
        if p.get("id") == prompt_id:
            prompts[i] = updated_data
            break
    save_data(data)

def delete_prompt(prompt_id: str):
    data = load_data()
    prompts = data.get("prompts", [])
    data["prompts"] = [p for p in prompts if p.get("id") != prompt_id]
    save_data(data)
