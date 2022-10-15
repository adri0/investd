import pandas as pd

from investd.metrics import invested_amount_by_col, total_invested
from investd.model import AssetType


def test_invested_amount(df_tx_minimal: pd.DataFrame):
    assert total_invested(df_tx_minimal) == 2349.0


def test_invested_amount_col(df_tx_minimal: pd.DataFrame):
    assert invested_amount_by_col(df_tx_minimal, "type").equals(
        pd.Series({AssetType.Stock: 849, AssetType.ETF: 1500})
    )
