from datetime import date
from typing import Any, Iterable

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from investd import views
from investd.common import AssetType as Asset
from investd.common import Currency as Cur


def test_total_invested_amount(df_tx_minimal: pd.DataFrame) -> None:
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
) -> None:
    assert views.invested_ref_amount_by_col(df_tx_minimal, col).equals(
        views.add_pct_col(views.to_nice_df(expected, ["PLN"]), "PLN")
    )


def _series_2levels_categorical_index(
    data: Iterable[Any], first_level: list[Any], second_level: list[Any]
) -> pd.Series:
    return pd.Series(
        data,
        index=pd.MultiIndex.from_product(
            [
                pd.Categorical(first_level),
                pd.Categorical(second_level),
            ]  # type: ignore
        ),
    ).dropna()


@pytest.mark.parametrize(
    "col, expected",
    [
        (
            "currency",
            pd.Series(
                data=[190.0, 300.0],
                index=pd.CategoricalIndex([Cur.USD, Cur.EUR]),  # type: ignore
            ),
        ),
        (
            "type",
            _series_2levels_categorical_index(
                data=[190.0, None, None, 300.0],
                first_level=[Cur.USD, Cur.EUR],
                second_level=[Asset.Stock, Asset.ETF],
            ),
        ),
        (
            "platform",
            _series_2levels_categorical_index(
                data=[190.0, None, None, 300.0],
                first_level=[Cur.USD, Cur.EUR],
                second_level=["revolut_stocks", "xtb"],
            ),
        ),
    ],
)
def test_invested_amount_currency_amount_col(
    df_tx_minimal: pd.DataFrame, col: str, expected: pd.Series
) -> None:
    actual = views.invested_amount_original_cur_by_col(df_tx_minimal, col)
    assert_series_equal(actual, expected, check_names=False)


def test_amounts_by_currency(df_tx_minimal: pd.DataFrame) -> None:
    expected = pd.DataFrame(
        {
            "Original currency": [190.0, 300.0],
            "PLN": [849, 1500],
            "%": [36.1, 63.9],
        },
        index=pd.CategoricalIndex([Cur.USD, Cur.EUR]),  # type: ignore
    )
    actual = views.amounts_by_currency(df_tx_minimal)
    assert_frame_equal(actual, expected, check_names=False)


@pytest.mark.parametrize(
    "period, expected",
    [
        (
            "YE",
            pd.DataFrame(
                {"PLN": [450, 1899], "Cumulated PLN": [450, 2349]},
                index=pd.PeriodIndex(["2021", "2022"], freq="Y"),
            ),
        ),
        (
            "ME",
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
) -> None:
    assert views.amount_over_time(df_tx_minimal, period).equals(expected)


def test_portfolio_value(
    df_tx_minimal: pd.DataFrame, df_quotes_minimal: pd.DataFrame
) -> None:
    at_date = date(2022, 1, 30)
    df_portfolio = views.portfolio_value(df_tx_minimal, df_quotes_minimal, at_date)
    expected = pd.DataFrame(
        {
            "Invested amount PLN": [450, 675, 1500],
            "Invested amount": [100.0, 150.0, 300.0],
            "Quantity": [2, 6, 2],
            "type": pd.Categorical([Asset.Stock, Asset.Stock, Asset.ETF]),
            "currency": pd.Categorical([Cur.USD, Cur.USD, Cur.EUR]),
            "platform": pd.Categorical(["revolut_stocks", "revolut_stocks", "xtb"]),
            "quote": [55.0, 20.0, 160.0],
            "Amount at date": [110.0, 120.0, 320.0],
            "Amount at date PLN": [506.0, 552.0, 1600.0],
        },
        index=pd.Index(["LOL", "TLDR", "XOXO"], name="symbol"),
    )
    assert_frame_equal(df_portfolio, expected)
