"""
    Functions for calculating portfolio metrics, such as net worth, etc.
"""

import pandas as pd

from .model import Action


def total_invested(df_tx: pd.DataFrame) -> float:
    """
    Calculates total invested amount in the reference currency.
    """
    return (
        df_tx[df_tx["action"] == Action.BUY]["amount_ref_currency"].sum()
        - df_tx[df_tx["action"] == Action.SELL]["amount_ref_currency"].sum()
    )


def invested_amount_by_asset_type(df_tx: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a DataFrame with invested amount by asset type in the reference currency.
    """
    return df_tx.groupby("type")["amount_ref_currency"].sum()
