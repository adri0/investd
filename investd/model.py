from datetime import datetime

from pydantic.dataclasses import dataclass

from enum import Enum


class Currency(Enum):
    USD = 1
    EUR = 2
    PLN = 3


class AssetType(Enum):
    ETF = 1
    Stock = 2
    Crypto = 3
    FX = 4


class Action(Enum):
    BUY = 1
    SELL = 2


@dataclass
class Transaction:
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