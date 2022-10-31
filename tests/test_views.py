from datetime import date
from typing import Any, Iterable

import pandas as pd
import pytest

from investd import views
from investd.model import AssetType as Asset
from investd.model import Currency as Cur


def test_total_invested_amount(df_tx_minimal: pd.DataFrame):
    assert views.total_invested_ref_currency(df_tx_minimal) == 2349.0


@pytest.mark.parametrize(
    "col, expected",
    [
        ("type", pd.Series({Asset.Stock: 849, Asset.ETF: 1500})),
        ("platform", pd.Series({"revolut_stocks": 849, "xtb": 1500})),
        ("symbol", pd.Series({"LOL": 174, "TLDR": 675, "XOXO": 1500})),
        ("currency", pd.Series({Cur.USD: 849, Cur.EUR: 1500})),
    ],
)
def test_invested_ref_amount_col(
    df_tx_minimal: pd.DataFrame, col: str, expected: pd.Series
):
    assert views.invested_ref_amount_by_col(df_tx_minimal, col).equals(
        views.add_pct_col(views.to_nice_df(expected, ["PLN"]), "PLN")
    )


def _multi_cat_series(
    values: Iterable[Any], first_level: Iterable[Any], second_level: Iterable[Any]
) -> pd.Series:
    return pd.Series(
        values,
        index=pd.MultiIndex.from_product(
            [
                pd.Categorical(first_level),
                pd.Categorical(second_level),
            ]
        ),
    )


@pytest.mark.parametrize(
    "col, expected",
    [
        ("currency", pd.Series({Cur.USD: 190.0, Cur.EUR: 300.0})),
        (
            "type",
            _multi_cat_series(
                [190.0, 0.0, 0.0, 300.0], [Cur.USD, Cur.EUR], [Asset.Stock, Asset.ETF]
            ),
        ),
        (
            "platform",
            _multi_cat_series(
                [190.0, 0.0, 0.0, 300.0], [Cur.USD, Cur.EUR], ["revolut_stocks", "xtb"]
            ),
        ),
    ],
)
def test_invested_amount_currency_amount_col(
    df_tx_minimal: pd.DataFrame, col: str, expected: pd.core.generic.NDFrame
):
    assert views.invested_amount_original_cur_by_col(df_tx_minimal, col).equals(
        expected
    )


def test_amounts_by_currency(df_tx_minimal: pd.DataFrame):
    expected = pd.DataFrame(
        {
            "Original currency": [190.0, 300.0],
            "PLN": [849, 1500],
            "%": [36.1, 63.9],
        },
        index=[Cur.USD, Cur.EUR],
    )
    assert views.amounts_by_currency(df_tx_minimal).equals(expected)


@pytest.mark.parametrize(
    "period, expected",
    [
        (
            "Y",
            pd.DataFrame(
                {"PLN": [450, 1899], "Cumulated PLN": [450, 2349]},
                index=pd.PeriodIndex(["2021", "2022"], freq="Y"),
            ),
        ),
        (
            "M",
            pd.DataFrame(
                {"PLN": [450, 2175, -276], "Cumulated PLN": [450, 2625, 2349]},
                index=pd.PeriodIndex(["2021-12", "2022-01", "2022-02"], freq="M"),
            ),
        ),
    ],
)
def test_amounts_over_time(
    df_tx_minimal: pd.DataFrame,
    period: str,
    expected: pd.DataFrame,
):
    assert views.amount_over_time(df_tx_minimal, period).equals(expected)
