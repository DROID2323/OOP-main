from abc import ABC, abstractmethod
from random import randint
from typing import List, Dict

# Абстрактний клас Asset
class Asset(ABC):
    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = float(amount)

    @abstractmethod
    def get_value_uah(self) -> float:
        pass

class CurrencyAsset(Asset):
    def __init__(self, name: str, amount: float, rate_to_uah: float):
        super().__init__(name, amount)
        self.__rate_to_uah = float(rate_to_uah)

    @property
    def rate(self) -> float:
        return self.__rate_to_uah

    def get_value_uah(self) -> float:
        return self.amount * self.__rate_to_uah

class CryptoAsset(Asset):
    def __init__(self, name: str, amount: float, base_rate_to_uah: float):
        super().__init__(name, amount)
        self.base_rate_to_uah = float(base_rate_to_uah)

    def get_value_uah(self) -> float:
        volatility = randint(-500, 500)
        effective_rate = max(0.0, self.base_rate_to_uah + volatility)
        return self.amount * effective_rate
    
class Portfolio:
    def __init__(self):
        self.__assets: List[Asset] = []

    def add(self, asset: Asset) -> None:
        self.__assets.append(asset)

    def total_value_uah(self) -> float:
        return sum(a.get_value_uah() for a in self.__assets)

    def list_assets(self) -> List[Dict]:
        return [
            {
                "type": a.__class__.__name__,
                "name": a.name,
                "amount": a.amount,
                "value_uah": round(a.get_value_uah(), 2)
            }
            for a in self.__assets
        ]