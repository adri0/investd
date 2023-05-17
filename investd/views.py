"""
    Portfolio metrics

    Functions for calculating portfolio metrics, such as net worth, etc.
"""

from datetime import date
from typing import Any, Iterable

import pandas as pd

from investd.common import Action
from investd.config import INVESTD_REF_CURRENCY


def _add_signed_cols(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Add columns ending with _signed to dataframe corresponding to
    negative sign to original amount column when action SELL.
    """
    cols = ("amount_ref_currency", "amount", "quantity")

    def get_signed_amount(row, col: str) -> float:
        return row[col] * (-1 if row["action"] == Action.SELL else 1)

    for col in cols:
        signed_col_name = col + "_signed"
        if signed_col_name in df_tx.columns:
            continue
        df_tx[signed_col_name] = df_tx.apply(get_signed_amount, axis=1, args=(col,))
    return df_tx


def total_invested_ref_currency(df_tx: pd.DataFrame) -> float:
    """
    Calculates total invested amount in the reference currency.
    """
    df_tx = _add_signed_cols(df_tx)
    return df_tx["amount_ref_currency_signed"].sum()


def to_nice_df(ndf: pd.core.generic.NDFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Transforms series into a nice looking dataframe in a notebook."""
    df = pd.DataFrame(ndf)
    df = df.applymap(round, ndigits=2)
    df.columns = pd.Index(columns).map(str)
    df.index.set_names(None, inplace=True)
    return df


def add_pct_col(
    df: pd.DataFrame, based_on_col: Any, pct_col_name: str = "%"
) -> pd.DataFrame:
    """Adds percentage column to dataframe."""
    df[pct_col_name] = round(df[based_on_col] / df[based_on_col].sum() * 100, ndigits=1)
    return df


def invested_ref_amount_by_col(df_tx: pd.DataFrame, col: str) -> pd.Series:
    """
    Generates a Series with invested amount by asset type in the reference currency.
    """
    df_tx = _add_signed_cols(df_tx)
    grouped = df_tx.groupby(col)["amount_ref_currency_signed"].sum()
    df = to_nice_df(grouped, columns=[str(INVESTD_REF_CURRENCY)])
    df = add_pct_col(df, based_on_col=str(INVESTD_REF_CURRENCY))
    return df


def amounts_by_currency(df_tx: pd.DataFrame) -> pd.Series:
    """
    Amounts aggregated by currency, showing invested amounts in
    original currency and reference currency.
    """
    df_tx = _add_signed_cols(df_tx)
    df_cur = df_tx.groupby("currency")[
        ["amount_signed", "amount_ref_currency_signed"]
    ].sum()
    df_cur = to_nice_df(
        df_cur, columns=["Original currency", str(INVESTD_REF_CURRENCY)]
    )
    df_cur = add_pct_col(df_cur, str(INVESTD_REF_CURRENCY))
    return df_cur


def invested_amount_original_cur_by_col(
    df_tx: pd.DataFrame, col: str
) -> pd.core.generic.NDFrame:
    """
    Aggregate invested amount by currency.
    """
    df_tx = _add_signed_cols(df_tx)
    grouping: list[str] | str = ["currency", col] if col != "currency" else col
    return df_tx.groupby(grouping)["amount_signed"].sum()


def amount_over_time(df_tx: pd.DataFrame, period: str) -> pd.DataFrame:
    """
    Amounts aggregate by periods over time.
    """
    df_tx = _add_signed_cols(df_tx)
    df_ot = (
        df_tx[["timestamp", "amount_ref_currency_signed"]]
        .groupby(pd.Grouper(key="timestamp", freq=period))
        .sum()
    )
    df_ot.index = df_ot.index.to_period()
    df_ot["cumsum"] = df_ot["amount_ref_currency_signed"].cumsum()
    df_ot = to_nice_df(
        df_ot, columns=[str(INVESTD_REF_CURRENCY), f"Cumulated {INVESTD_REF_CURRENCY}"]
    )
    return df_ot


def portfolio_value(
    df_tx: pd.DataFrame, df_quotes: pd.DataFrame, at_date: date
) -> pd.DataFrame:
    df_tx = _add_signed_cols(df_tx)
    df_tx = df_tx[df_tx["timestamp"] <= pd.Timestamp(at_date)]
    df_portfolio = df_tx.groupby("symbol").agg(
        {
            "amount_ref_currency_signed": "sum",
            "amount_signed": "sum",
            "quantity_signed": "sum",
            "type": "first",
            "currency": "first",
            "platform": "first",
        }
    )
    df_quotes_date = df_quotes[
        pd.to_datetime(df_quotes["date"]) == pd.Timestamp(at_date)
    ]
    quotes = df_quotes_date.set_index("symbol")["price"]
    df_portfolio["quote"] = df_portfolio.index.map(quotes)
    df_portfolio["amount_at_date"] = (
        df_portfolio["quote"] * df_portfolio["quantity_signed"]
    )
    exchange_rate_to_ref_cur = (
        df_portfolio["currency"]
        .map(
            lambda cur: quotes.get(f"{cur}{INVESTD_REF_CURRENCY}=X")
            if cur != INVESTD_REF_CURRENCY
            else 1
        )
        .astype(float)
    )
    df_portfolio["amount_at_date_ref_currency"] = (
        df_portfolio["amount_at_date"] * exchange_rate_to_ref_cur
    )
    df_portfolio = df_portfolio.rename(
        {
            "amount_at_date": "Amount at date",
            "amount_at_date_ref_currency": f"Amount at date {INVESTD_REF_CURRENCY}",
            "amount_signed": "Invested amount",
            "amount_ref_currency_signed": f"Invested amount {INVESTD_REF_CURRENCY}",
            "quantity_signed": "Quantity",
        },
        axis=1,
    )
    return df_portfolio
