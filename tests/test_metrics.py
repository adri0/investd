import pandas as pd
import pytest

from investd.metrics import invested_ref_amount_by_col, total_invested_ref_currency
from investd.model import AssetType, Currency


def test_invested_amount(df_tx_minimal: pd.DataFrame):
    assert total_invested_ref_currency(df_tx_minimal) == 2349.0


@pytest.mark.parametrize(
    "col,expected_result",
    [
        ("type", pd.Series({AssetType.Stock: 849, AssetType.ETF: 1500})),
        ("platform", pd.Series({"revolut_stocks": 849, "xtb": 1500})),
        ("symbol", pd.Series({"LOL": 174, "TLDR": 675, "XOXO": 1500})),
        ("currency", pd.Series({Currency.USD: 849, Currency.EUR: 1500})),
    ],
)
def test_invested_ref_amount_col(
    df_tx_minimal: pd.DataFrame, col: str, expected_result: pd.core.generic.NDFrame
):
    assert invested_ref_amount_by_col(df_tx_minimal, col).equals(expected_result)
