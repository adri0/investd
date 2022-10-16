import pandas as pd
import pytest

from investd.metrics import (
    invested_amount_original_currency_by_col,
    invested_ref_amount_by_col,
    total_invested_ref_currency,
)
from investd.model import AssetType, Currency


def test_total_invested_amount(df_tx_minimal: pd.DataFrame):
    assert total_invested_ref_currency(df_tx_minimal) == 2349.0


@pytest.mark.parametrize(
    "col,expected",
    [
        ("type", pd.Series({AssetType.Stock: 849, AssetType.ETF: 1500})),
        ("platform", pd.Series({"revolut_stocks": 849, "xtb": 1500})),
        ("symbol", pd.Series({"LOL": 174, "TLDR": 675, "XOXO": 1500})),
        ("currency", pd.Series({Currency.USD: 849, Currency.EUR: 1500})),
    ],
)
def test_invested_ref_amount_col(
    df_tx_minimal: pd.DataFrame, col: str, expected: pd.Series
):
    assert invested_ref_amount_by_col(df_tx_minimal, col).equals(expected)


@pytest.mark.parametrize(
    "col,expected",
    [
        ("currency", pd.Series({Currency.USD: 190.0, Currency.EUR: 300.0})),
        (
            "type",
            pd.Series(
                {
                    (Currency.USD, AssetType.Stock): 190.0,
                    (Currency.USD, AssetType.ETF): 0.0,
                    (Currency.EUR, AssetType.Stock): 0.0,
                    (Currency.EUR, AssetType.ETF): 300.0,
                }
            ),
        ),
        (
            "platform",
            pd.Series(
                {
                    (Currency.USD, "revolut_stocks"): 190.0,
                    (Currency.USD, "xtb"): 0.0,
                    (Currency.EUR, "revolut_stocks"): 0.0,
                    (Currency.EUR, "xtb"): 300.0,
                }
            ),
        ),
    ],
)
def test_invested_amount_currency_amount_col(
    df_tx_minimal: pd.DataFrame, col: str, expected: pd.core.generic.NDFrame
):
    ndf = invested_amount_original_currency_by_col(df_tx_minimal, col)
    assert expected.equals(ndf)
