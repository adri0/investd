from datetime import datetime

from pydantic.dataclasses import dataclass

from .misc import StringEnum


Currency = StringEnum("Currency", "USD EUR PLN")

AssetType = StringEnum("AssetType", "ETF Stock Crypto Currency")


@dataclass
class Transaction:
    id: str
    timestamp: datetime
    symbol: str
    type: AssetType  # type: ignore
    platform: str
    currency: Currency  # type: ignore
    amount: float
    quantity: float
    price: float
    exchange_rate: float
    amount_ref_currency: float
    action: str


@dataclass
class Portfolio:
    to_date: datetime
    total_invested: float


@dataclass
class AssetInvested:
    symbol: str
    type: AssetType  # type: ignore
    currency: Currency  # type: ignore
    quantity: float
    amount: float
    amount_ref_cur: float

