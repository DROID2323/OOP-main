import json
from pathlib import Path
from typing import Dict, Any

from google.adk.agents import ParallelAgent, SequentialAgent, LoopAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext

MODEL = "gemini-3.1-flash-lite-preview"

STATE_SOURCES = "sources"
STATE_CLEAN = "cleaned"
STATE_ANALYSIS = "analysis"
STATE_DRAFT = "draft"
STATE_FINAL = "final_report"
COMPLETION_PHRASE = "ЗВІТ ГОТОВ"

STATE_FILE = Path("combined_workflow/state.json")
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

def save_state(data: Dict[str, Any]):
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

fetch_a = Agent(
    name="FetchSourceA",
    model=MODEL,
    instruction="""
    Збери дані з джерела A (імітація). Поверни JSON-рядок з ключем 'data' і списком елементів.
    """,
    description="Збір даних з джерела A",
    output_key="source_a"
)

fetch_b = Agent(
    name="FetchSourceB",
    model=MODEL,
    instruction="""
    Збери дані з джерела B (імітація). Поверни JSON-рядок з ключем 'data' і списком елементів.
    """,
    description="Збір даних з джерела B",
    output_key="source_b"
)

fetch_c = Agent(
    name="FetchSourceC",
    model=MODEL,
    instruction="""
    Збери дані з джерела C (імітація). Поверни JSON-рядок з ключем 'data' і списком елементів.
    """,
    description="Збір даних з джерела C",
    output_key="source_c"
)

parallel_fetch = ParallelAgent(
    name="ParallelFetch",
    sub_agents=[fetch_a, fetch_b, fetch_c],
    description="Паралельний збір даних з трьох джерел"
)
cleaner = Agent(
    name="Cleaner",
    model=MODEL,
    instruction="""
    Отримай з контексту source_a, source_b, source_c (JSON). Об'єднай списки в один список 'cleaned'.
    Поверни JSON з ключем 'cleaned'.
    """,
    description="Очищення і злиття даних",
    output_key=STATE_CLEAN
)

analyzer = Agent(
    name="Analyzer",
    model=MODEL,
    instruction=f"""
    Отримай 'cleaned' зі стану. Зроби простий аналіз: підрахуй кількість елементів і склади короткий summary.
    Поверни JSON з ключами 'count' і 'summary'.
    """,
    description="Аналіз очищених даних",
    output_key=STATE_ANALYSIS
)

drafter = Agent(
    name="Drafter",
    model=MODEL,
    instruction=f"""
    На основі 'summary' і 'count' склади чернетку звіту (2-4 речення).
    Поверни ТІЛЬКИ текст звіту у полі 'draft'.
    """,
    description="Складання чернетки звіту",
    output_key=STATE_DRAFT
)

sequential_pipeline = SequentialAgent(
    name="ProcessAndDraft",
    sub_agents=[cleaner, analyzer, drafter],
    description="Очищення → аналіз → складання чернетки"
)

def exit_loop(tool_context: ToolContext):
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    return {}
critic = Agent(
    name="ReportCritic",
    model=MODEL,
    instruction=f"""
    Ти критик звітів. Оціни текст у {{draft}}.
    Критерії завершення (всі мають бути виконані):
    1) Мінімум 4 речення
    2) Є вступ, основна частина і висновок
    3) Є хоча б одна конкретна деталь або приклад

    Якщо всі критерії виконано — відповідай ТІЛЬКИ: "{COMPLETION_PHRASE}"
    Інакше — дай коротку конкретну критику (1-2 речення), що треба додати.
    """,
    description="Критика чернетки",
    output_key="critique"
)

improver = Agent(
    name="ReportImprover",
    model=MODEL,
    instruction=f"""
    Ти редактор. Отримай {{draft}} і {{critique}}.
    Якщо critique точно "{COMPLETION_PHRASE}" — викликай exit_loop (не виводь текст).
    Інакше — застосуй критику і поверни покращену версію draft у полі 'draft'.
    """,
    description="Покращення чернетки",
    tools=[exit_loop],
    output_key=STATE_DRAFT
)

improvement_loop = LoopAgent(
    name="ImproveReportLoop",
    sub_agents=[critic, improver],
    max_iterations=5,
    description="Ітеративне покращення чернетки до якості"
)

root_agent = SequentialAgent(
    name="CombinedWorkflow",
    sub_agents=[parallel_fetch, sequential_pipeline, improvement_loop],
    description="Parallel збір → Sequential обробка → Loop покращення"
)

if __name__ == "__main__":
    print("Запускаю CombinedWorkflow локально (через ADK CLI запускай: poetry run adk run CombinedWorkflow)")