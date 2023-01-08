from typing import Type

import pandas as pd

from investd.sources.base import SourceBase
from investd.transaction import Transaction

from . import bonds, bossa, revolut_stocks, xtb

sources: list[Type[SourceBase]] = [
    xtb.XTB,
    revolut_stocks.RevolutStocks,
    bonds.Bonds,
    bossa.Bossa,
]


def ingest_sources_as_df() -> pd.DataFrame:
    df_tx = pd.DataFrame(columns=Transaction.__dataclass_fields__.keys())
    for source_class in sources:
        source = source_class()
        df_tx = pd.concat(
            [df_tx, pd.DataFrame([tx for tx in source.load_transactions()])]
        )
    df_tx.sort_values(by="timestamp", ascending=True, inplace=True)
    return df_tx
