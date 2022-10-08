"""
    Portfolio

    Functions for calcuating portfolio metrics, such as net worth, etc.
"""

import pandas as pd

from .model import Action


def total_net_worth(df_tx: pd.DataFrame) -> float:
    """
    Calulates net worth of a portfolio in the reference currency.
    """
    return (
        df_tx[df_tx["action"] == Action.BUY]["amount_ref_currency"].sum()
        + df_tx[df_tx["action"] == Action.SELL]["amount_ref_currency"].sum()
    )


def net_worth_by_asset_type(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Calulates net worth of a portfolio by asset type and returns a DataFrame.
    """
    return df_tx.groupby("type")["amount_ref_currency"].sum()
