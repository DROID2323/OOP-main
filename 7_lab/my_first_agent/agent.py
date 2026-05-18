import logging
import datetime
from google.adk.agents.llm_agent import Agent

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Інструмент для отримання часу
def get_current_time(city: str) -> dict:
    """
    Повертає поточний час у вказаному місті.
    """
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    logger.info(f"Виклик get_current_time для міста: {city}")
    return {
        "status": "success",
        "city": city,
        "time": current_time
    }

# Інструмент для логування
def logging_tool(param: str) -> dict:
    """Інструмент з логуванням подій"""
    logger.info(f"Виклик logging_tool з параметром: {param}")
    return {"result": "success", "processed_param": param}

# Створюємо агента
root_agent = Agent(
    model='gemini-3.1-flash-lite-preview',
    name='time_logging_agent',
    description="Агент, який повідомляє час і веде логування.",
    instruction="""
    Ти корисний асистент, який повідомляє поточний час у містах
    та логує всі виклики інструментів. Відповідай українською мовою
    у форматі HH:MM:SS.
    """,
    tools=[get_current_time, logging_tool],
)
