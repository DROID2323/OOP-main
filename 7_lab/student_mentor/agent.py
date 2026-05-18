import logging
from google.adk.agents.llm_agent import Agent
from tools.common_tools import (
    explain_concept,
    check_syntax,
    format_text,
    count_words,
    safe_divide,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("student_mentor")

def explain_concept_tool(concept: str, level: str = "beginner") -> dict:
    """
    Обгортка для explain_concept з логуванням та обробкою помилок.

    Args:
        concept: назва концепції
        level: рівень пояснення (beginner|intermediate|advanced)

    Returns:
        dict: структурований результат від explain_concept або помилка
    """
    logger.info("Виклик explain_concept_tool concept=%s level=%s", concept, level)
    try:
        result = explain_concept(concept, level)
        return result
    except Exception as e:
        logger.exception("Помилка в explain_concept_tool")
        return {"status": "error", "message": str(e)}

def check_syntax_tool(code: str, language: str = "python") -> dict:
    """
    Обгортка для check_syntax з логуванням та обробкою помилок.

    Args:
        code: рядок коду для перевірки
        language: мова програмування

    Returns:
        dict: результат перевірки або помилка
    """
    logger.info("Виклик check_syntax_tool language=%s", language)
    try:
        result = check_syntax(code, language)
        return result
    except Exception as e:
        logger.exception("Помилка в check_syntax_tool")
        return {"status": "error", "message": str(e)}

def safe_divide_tool(a, b) -> dict:
    """
    Обгортка для safe_divide з логуванням.

    Args:
        a: ділене
        b: дільник

    Returns:
        dict: {status, result, error}
    """
    logger.info("Виклик safe_divide_tool a=%s b=%s", a, b)
    try:
        return safe_divide(a, b)
    except Exception as e:
        logger.exception("Помилка в safe_divide_tool")
        return {"status": "error", "result": None, "error": str(e)}

root_agent = Agent(
    model="gemini-3.1-flash-lite-preview",
    name="student_mentor",
    description="Агент-ментор для студентів: пояснює концепції, перевіряє синтаксис, форматує текст і виконує прості обчислення.",
    instruction="""
Ти досвідчений викладач програмування. Відповідай українською мовою.
Коли користувач просить пояснити концепцію — виклич explain_concept_tool(concept, level).
Коли користувач просить перевірити код — виклич check_syntax_tool(code, language).
Коли користувач просить поділити числа — виклич safe_divide_tool(a, b).
Формат відповіді:
  1) Короткий висновок (1-2 речення).
  2) Блок коду у Markdown якщо є приклад.
  3) Структурований підсумок (dict) з полями status, message, details або result.
""",
    tools=[explain_concept_tool, check_syntax_tool, safe_divide_tool, format_text, count_words],
)