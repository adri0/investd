"""
    Portfolio metrics

    Functions for calculating portfolio metrics, such as net worth, etc.
"""

from typing import Any, Iterable

import pandas as pd

from .config import REF_CURRENCY
from .model import Action


def _add_signed_cols(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Add columns ending with _signed to dataframe corresponding to
    negative sign to original amount column when action SELL.
    """
    cols = ("amount_ref_currency", "amount")

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


def add_pct_col(df: pd.DataFrame, based_on_col: Any) -> pd.DataFrame:
    """Adds percentage column to dataframe."""
    df[f"% ({based_on_col})"] = round(
        df[based_on_col] / df[based_on_col].sum() * 100, ndigits=1
    )
    return df


def invested_ref_amount_by_col(df_tx: pd.DataFrame, col: str) -> pd.Series:
    """
    Generates a Series with invested amount by asset type in the reference currency.
    """
    df_tx = _add_signed_cols(df_tx)
    grouped = df_tx.groupby(col)["amount_ref_currency_signed"].sum()
    df = to_nice_df(grouped, columns=[str(REF_CURRENCY)])
    df = add_pct_col(df, based_on_col=str(REF_CURRENCY))
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
    df_cur = to_nice_df(df_cur, columns=["Original currency", str(REF_CURRENCY)])
    df_cur = add_pct_col(df_cur, str(REF_CURRENCY))
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
