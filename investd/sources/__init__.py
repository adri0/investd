from typing import Type

import pandas as pd

from ..sources.base import SourceBase
from ..transactions import Transaction
from . import revolut_stocks, xtb

sources: list[Type[SourceBase]] = [xtb.XTB, revolut_stocks.RevolutStocks]


def ingest_sources_as_df() -> pd.DataFrame:
    df_tx = pd.DataFrame(columns=Transaction.__dataclass_fields__.keys())
    for source_class in sources:
        source = source_class()
        df_tx = pd.concat(
            [df_tx, pd.DataFrame([tx for tx in source.load_transactions()])]
        )
    df_tx.sort_values(by="timestamp", ascending=True, inplace=True)
    return df_tx
