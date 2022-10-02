from datetime import datetime
from enum import Enum

from pydantic.dataclasses import dataclass


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"


class AssetType(Enum):
    ETF = "ETF"
    Stock = "Stock"
    Crypto = "Crypto"
    FX = "FX"


class Action(Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass
class Transaction:
    id: str
    timestamp: datetime
    symbol: str
    type: AssetType
    platform: str
    currency: Currency
    amount: float
    quantity: float
    price: float
    exchange_rate: float
    amount_ref_currency: float
    action: Action


@dataclass
class Portfolio:
    to_date: datetime
    total_invested: float


@dataclass
class AssetInvested:
    symbol: str
    type: AssetType
    currency: Currency
    quantity: float
    amount: float
    amount_ref_cur: float


@dataclass
class ExchangeRate:
    timestamp: datetime
    currency_from: Currency
    currency_to: Currency
