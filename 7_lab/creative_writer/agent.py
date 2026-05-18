from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

def generate_story_prompt(theme: str, characters: int = 2) -> str:
    """
    Генерує промпт для історії.
    
    Args:
        theme: тема історії
        characters: кількість персонажів
    
    Returns:
        str: промпт для генерації історії
    """
    return f"Створи цікаву історію на тему '{theme}' з {characters} персонажами."

root_agent = Agent(
    model='gemini-3.1-flash-lite-preview',
    name='creative_writer',
    description="Креативний письменник історій.",
    instruction="""
    Ти талановитий письменник який створює захоплюючі історії.
    Твої історії мають бути:
    - Цікавими та захоплюючими
    - З несподіваними поворотами сюжету
    - З яскравими персонажами
    - Написаними українською мовою
    
    Використовуй багатий словниковий запас та літературні прийоми.
    """,
    tools=[generate_story_prompt],
)