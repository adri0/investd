from dataclasses import Field
from datetime import datetime
from enum import Enum
from typing import Any

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


def to_pandas_schema(data_class: type) -> dict[str, Any]:
    def to_pandas_dtype(field: Field) -> Any:
        if field.type is datetime:
            return "datetime64[ns]"
        if issubclass(field.type, Enum):
            return pd.CategoricalDtype(field.type.__members__.values())
        return field.type

    return {
        field.name: to_pandas_dtype(field)
        for field in data_class.__dataclass_fields__.values()  # type: ignore
    }


def categorical_fields(data_class: type) -> dict[str, type[Enum]]:
    return {
        field.name: field.type
        for field in data_class.__dataclass_fields__.values()  # type: ignore
        if issubclass(field.type, Enum)
    }


def load_transactions() -> pd.DataFrame:
    path = PERSIST_PATH / "tx.csv"
    df_tx = pd.read_csv(path, converters=categorical_fields(Transaction))
    schema = to_pandas_schema(Transaction)
    df_tx = df_tx.astype(schema)
    return df_tx
