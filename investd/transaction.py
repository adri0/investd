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


def load_transactions() -> pd.DataFrame:
    """Load transactions in persistence as a DataFrame."""
    path = PERSIST_PATH / "tx.csv"
    df_tx = pd.read_csv(path, converters=_enum_fields(Transaction))
    schema = _to_pandas_schema(Transaction)
    return df_tx.astype(schema)


def _enum_fields(data_class: type) -> dict[str, type[Enum]]:
    """Return a dict of enum fields in a dataclass."""
    return {
        field.name: field.type
        for field in data_class.__dataclass_fields__.values()  # type: ignore
        if issubclass(field.type, Enum)
    }


def _to_pandas_schema(data_class: type) -> dict[str, type | str]:
    """Convert a dataclass to a pandas dtype schema."""

    def to_pandas_dtype(field: Field) -> Any:
        if field.type is datetime:
            return "datetime64[ns]"
        elif issubclass(field.type, Enum):
            return pd.CategoricalDtype(field.type.__members__.values())
        else:
            return field.type

    return {
        field.name: to_pandas_dtype(field)
        for field in data_class.__dataclass_fields__.values()  # type: ignore
    }
