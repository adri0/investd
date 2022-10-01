import re
from pathlib import Path
from typing import Iterator

import pandas as pd

from ..model import AssetType, Currency, Transaction
from .base import SourceBase

currency_by_symbol = {
    "INR.FR": Currency.EUR,
    "BETASPXP.PL": Currency.PLN,
    "V80A.DE": Currency.EUR,
    "ETFBWTECH.PL": Currency.PLN,
    "CSPX.UK": Currency.USD,
    "VHYD.UK": Currency.USD
}


class XTB(SourceBase):

    source_name = "xtb"

    def parse_source_file(self, path: Path) -> Iterator[Transaction]:
        df = pd.read_excel(
            path, 
            sheet_name="CASH OPERATION HISTORY",        
            skiprows=10, 
            usecols=["ID", "Type", "Time", "Comment", "Symbol", "Amount"],
            parse_dates=["Time"]
        )
        df = df[~pd.isna(df["Symbol"])]
        return map(lambda i_row: self._convert(i_row[1]), df.iterrows())

    @staticmethod
    def parse_comment(comment: str) -> tuple[str, float, float]:
        for match in re.finditer(r"(?P<action>BUY|SELL) (?P<quantity>[\d\.]+) @ (?P<price>[\d\.]+)", comment):
            return match["action"], float(match["quantity"]), float(match["price"])
        raise ValueError(f"No matches found for comment pattern in Comment: {comment}")

    def _convert(self, record: pd.Series) -> Transaction:
        action, quantity, price = XTB.parse_comment(record["Comment"])
        return Transaction(
            id=record["ID"],
            timestamp=record["Time"],
            symbol=record["Symbol"],
            type=AssetType.ETF,
            platform="XTB",
            currency=currency_by_symbol[record["Symbol"]],
            amount=price * quantity,
            quantity=quantity,
            price=price,
            exchange_rate=abs(record["Amount"]) / price / quantity,
            amount_ref_currency=abs(record["Amount"]),
            action=action.lower()
        )
