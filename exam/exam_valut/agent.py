import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from .oop import CurrencyAsset, CryptoAsset, Portfolio

load_dotenv()

FIXED_RATES_TO_UAH = {
    "USD": 41.5,
    "EUR": 45.0,
    "GBP": 52.0,
    "BTC": 3_800_000.0
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in FIXED_RATES_TO_UAH:
        return {"status": "error", "message": f"Невідомий курс: {from_currency}"}
    if to_currency not in FIXED_RATES_TO_UAH:
        return {"status": "error", "message": f"Невідомий курс: {to_currency}"}

    rate_from = FIXED_RATES_TO_UAH[from_currency]
    rate_to = FIXED_RATES_TO_UAH[to_currency]

    asset = CurrencyAsset(from_currency, amount, rate_from)
    value_uah = asset.get_value_uah()
    result = value_uah / rate_to if rate_to else 0.0

    return {
        "status": "success",
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "result": result,
        "rate": {"from_to_uah": rate_from, "to_to_uah": rate_to}
    }

instruction_text = (
    "Ви фінансовий консультант з обміну валют. "
    "Відповідайте українською, пояснюйте курс і робіть конвертацію "
    "через інструмент convert_currency."
)

root_agent = Agent(
    model=os.getenv("ADK_MODEL", "gemini-2.5-flash"),
    name="currency_agent_variant_5",
    description="Агент конвертації валют. Відповідає українською.",
    instruction=instruction_text,
    tools=[convert_currency],
)
