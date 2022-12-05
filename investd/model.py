from datetime import datetime
from enum import Enum
from os import PathLike

import numpy as np
import pandas as pd
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

    @classmethod
    def from_csv(cls, path: PathLike) -> pd.DataFrame:
        df_tx = pd.read_csv(
            path,
            converters={
                name: field.type if field.type not in (datetime,) else pd.to_datetime
                for name, field in Transaction.__dataclass_fields__.items()
            },
        )
        categories = ("type", "platform", "currency", "action")
        for cat in categories:
            df_tx[cat] = df_tx[cat].astype("category")
        return df_tx


@dataclass
class ExchangeRate:
    timestamp: datetime
    currency_from: Currency
    currency_to: Currency
