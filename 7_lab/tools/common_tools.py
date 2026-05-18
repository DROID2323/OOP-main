# tools/common_tools.py
"""Спільні інструменти для агентів.

Кожна функція має докладний docstring, валідацію вхідних даних,
обробку помилок і повертає структуровані дані (dict або str).
"""

from typing import Dict, Any
import ast


def format_text(text: str, style: str = "uppercase") -> str:
    """
    Форматує текст.

    Args:
        text: вхідний текст
        style: 'uppercase'|'lowercase'|'title'|'none'

    Returns:
        Відформатований рядок.

    Raises:
        TypeError якщо text не рядок.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    style = (style or "none").lower()
    if style == "uppercase":
        return text.upper()
    if style == "lowercase":
        return text.lower()
    if style == "title":
        return text.title()
    return text


def count_words(text: str) -> Dict[str, Any]:
    """
    Підраховує слова і символи.

    Args:
        text: вхідний текст

    Returns:
        dict: {status, total_words, total_chars, unique_words}
    """
    if not isinstance(text, str):
        return {"status": "error", "message": "text must be a string"}
    words = text.split()
    return {
        "status": "success",
        "total_words": len(words),
        "total_chars": len(text),
        "unique_words": len(set(words)),
    }


def explain_concept(concept: str, level: str = "beginner") -> Dict[str, Any]:
    """
    Пояснює концепцію на трьох рівнях.

    Args:
        concept: назва концепції
        level: 'beginner'|'intermediate'|'advanced'

    Returns:
        dict: {status, concept, level, explanation, example}
    """
    if not concept or not isinstance(concept, str):
        return {"status": "error", "message": "concept must be a non-empty string"}
    lvl = (level or "beginner").lower()
    explanations = {
        "beginner": f"{concept}: коротке просте пояснення зрозумілою мовою.",
        "intermediate": f"{concept}: поглиблене пояснення з прикладами.",
        "advanced": f"{concept}: детальне технічне пояснення з крайовими випадками.",
    }
    examples = {
        "beginner": f"# Приклад для {concept}\nprint('Hello, world')",
        "intermediate": f"# Поглиблений приклад для {concept}\ndef example():\n    pass",
        "advanced": f"# Просунутий приклад для {concept}\nclass AdvancedExample:\n    pass",
    }
    explanation = explanations.get(lvl, explanations["beginner"])
    example = examples.get(lvl, examples["beginner"])
    return {
        "status": "success",
        "concept": concept,
        "level": lvl,
        "explanation": explanation,
        "example": example,
    }


def check_syntax(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Перевіряє синтаксис коду. Для Python використовує ast.parse.

    Args:
        code: рядок коду
        language: мова програмування

    Returns:
        dict: {status, message, details?}
    """
    if not code or not isinstance(code, str):
        return {"status": "error", "message": "code must be a non-empty string"}
    lang = (language or "python").lower()
    if lang == "python":
        try:
            ast.parse(code)
            return {"status": "success", "message": "Синтаксис Python виглядає коректно"}
        except SyntaxError as e:
            return {
                "status": "error",
                "message": "Синтаксична помилка в Python-коді",
                "details": f"{e.msg} (рядок {e.lineno}, колонка {e.offset})",
            }
    return {"status": "not_implemented", "message": f"Перевірка для мови '{language}' не реалізована"}


def safe_divide(a: float, b: float) -> Dict[str, Any]:
    """
    Ділить два числа з перевіркою на нуль і типи.

    Args:
        a: ділене
        b: дільник

    Returns:
        dict: {status, result, error}
    """
    try:
        a_val = float(a)
        b_val = float(b)
    except Exception:
        return {"status": "error", "result": None, "error": "Невірні типи: очікується числа"}
    if b_val == 0:
        return {"status": "error", "result": None, "error": "Ділення на нуль неможливе"}
    return {"status": "success", "result": a_val / b_val, "error": None}