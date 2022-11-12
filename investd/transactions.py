from datetime import datetime
from os import PathLike

import pandas as pd
from pydantic.dataclasses import dataclass

from .common import Action, AssetType, Currency
from .config import PERSIST_PATH


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


def load_transactions() -> pd.DataFrame:
    path = PERSIST_PATH / "tx.csv"
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
