import re
from pathlib import Path
from typing import Iterator

import pandas as pd

from investd.common import Action, AssetType, Currency
from investd.sources.base import SourceBase
from investd.transaction import Transaction

COL_AMOUNT = "Amount"
COL_COMMENT = "Comment"
COL_ID = "ID"
COL_SYMBOL = "Symbol"
COL_TIME = "Time"
COL_TYPE = "Type"

INPUT_COLUMNS = [COL_AMOUNT, COL_COMMENT, COL_ID, COL_SYMBOL, COL_TIME, COL_TYPE]


class XTB(SourceBase):
    source_name = "xtb"

    def parse_source_file(self, path: Path) -> Iterator[Transaction]:
        if path.suffix == ".xlsx":
            df = pd.read_excel(
                path,
                sheet_name="CASH OPERATION HISTORY",
                skiprows=10,
                usecols=INPUT_COLUMNS,
                parse_dates=[COL_TIME],
            )
        elif path.suffix == ".csv":
            df = pd.read_csv(
                path, usecols=INPUT_COLUMNS, parse_dates=[COL_TIME], sep=";"
            )
        else:
            return []

        df = df[~pd.isna(df[COL_SYMBOL])]
        return map(lambda i_row: self._convert(i_row[1]), df.iterrows())

    def _convert(self, record: pd.Series) -> Transaction:
        action, quantity, price = XTB.parse_comment(record[COL_COMMENT])
        return Transaction(
            id=record[COL_ID],
            timestamp=record[COL_TIME],
            symbol=record[COL_SYMBOL],
            type=AssetType.ETF,
            platform=self.source_name,
            currency=XTB.infer_currency_from_symbol(record[COL_SYMBOL]),
            amount=price * quantity,
            quantity=quantity,
            price=price,
            exchange_rate=abs(record[COL_AMOUNT]) / price / quantity,
            amount_ref_currency=abs(record[COL_AMOUNT]),
            action=Action(action.upper()),
        )

    @staticmethod
    def parse_comment(comment: str) -> tuple[str, float, float]:
        for match in re.finditer(
            r"(?P<action>BUY|SELL) (?P<quantity>[\d.]+)(/\d+)? @ (?P<price>[\d.]+)",
            comment,
        ):
            return match["action"], float(match["quantity"]), float(match["price"])
        raise ValueError(
            f"No matches found for comment pattern in Comment: '{comment}'"
        )

    @staticmethod
    def infer_currency_from_symbol(symbol: str) -> Currency:
        _, country = symbol.split(".")
        if country in ("UK", "US"):
            return Currency.USD
        elif country == "PL":
            return Currency.PLN
        else:
            return Currency.EUR
