from datetime import datetime
from enum import Enum

from pydantic.dataclasses import dataclass


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"

    def __str__(self) -> str:
        return self.name


class AssetType(Enum):
    ETF = "ETF"
    Stock = "Stock"
    Crypto = "Crypto"
    FX = "FX"
    Bond = "Bond"

    def __str__(self) -> str:
        return self.name


class Action(Enum):
    BUY = "BUY"
    SELL = "SELL"

    def __str__(self) -> str:
        return self.name


@dataclass
class ExchangeRate:
    timestamp: datetime
    currency_from: Currency
    currency_to: Currency
