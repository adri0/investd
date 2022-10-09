from typing import Type

import pandas as pd

from investd.model import Transaction
from investd.sources.base import SourceBase

from . import revolut_stocks, xtb

sources: list[Type[SourceBase]] = [xtb.XTB, revolut_stocks.RevolutStocks]


def ingest_sources_as_df() -> pd.DataFrame:
    df_tx = pd.DataFrame(columns=Transaction.__dataclass_fields__.keys())
    for source_class in sources:
        source = source_class()
        df_tx = pd.concat(
            [df_tx, pd.DataFrame([tx for tx in source.load_transactions()])]
        )
    return df_tx
