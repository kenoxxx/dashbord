import re
import tiktoken

# Регулярное выражение для поиска переменных вида {{переменная}}
VARIABLE_REGEX = re.compile(r"\{\{([^}]+)\}\}")

def extract_variables(template: str) -> list[str]:
    """Извлекает список уникальных переменных из шаблона."""
    if not template:
        return []
    matches = VARIABLE_REGEX.findall(template)
    # Удаляем пробелы по краям и сохраняем уникальность
    return list(dict.fromkeys(m.strip() for m in matches))

def build_prompt(template: str, variables: dict[str, str]) -> str:
    """Подставляет значения переменных в шаблон."""
    if not template:
        return ""
        
    result = template
    for var, val in variables.items():
        # Регулярка для замены этой конкретной переменной, учитывая возможные пробелы {{ var }}
        pattern = r"\{\{\s*" + re.escape(var) + r"\s*\}\}"
        result = re.sub(pattern, val, result)
        
    return result

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Подсчитывает количество токенов в тексте для указанной модели LLM."""
    if not text:
        return 0
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
